from conn.connector import DBConnector
import json
import sys, time
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily


class CustomCollector(object):

    def int_value(self,value):
        none, value = value.split("[(")
        value, none = value.split(",)]")
        return value

    def str_value(self,value):
        value = str(value)
        none, value = value.split("('")
        value, none = value.split("',)")
        value = value.replace("-","_")
        return value


    def collect(self):
        self.configure()
        con = DBConnector(self.db_name,self.db_user,
                self.db_password,self.db_host,self.db_port, self.db_type)
        for metric in self.metrics:
            metric_type = self.metrics[metric]["type"]
            metric_query = self.metrics[metric]["query"]
            metric_datatype = self.metrics[metric]["datatype"]
            #print(metric_query)
            if metric_type == 'gauge':
                label = self.metrics[metric]["label"]
                values = self.metrics[metric]["values"]
                help = self.metrics[metric]["help"]
                result = con.read_query(metric_query)
                if metric_datatype == "int":
                    stat = GaugeMetricFamily(values, help, labels = [label])
                    result = self.int_value(str(result))
                    stat.add_metric('', result)
                    print(metric,result)
                    yield stat
                if metric_datatype == "str":
                    for item in result:
                        #print("item:",item)
                        item = self.str_value(item)
                        #print("item:", item)
                        stat = GaugeMetricFamily(values, help, labels = [label])
                        stat.add_metric([item], '1')
                        print(values,item)
                        yield stat

            if metric_type == "counter":
                label = self.metrics[metric]["label"]
                values = self.metrics[metric]["values"]
                help = self.metrics[metric]["help"]
                result = con.read_query(metric_query)
                if metric_datatype == "int":
                    stat = CounterMetricFamily(values, help, labels = [label])
                    result = self.int_value(str(result))
                    stat.add_metric('', result)
                    print(metric,result)
                    yield stat
                if metric_datatype == "str":
                    for item in result:
                        #print("item:",item)
                        item = self.str_value(item)
                        #print("item:", item)
                        stat = CounterMetricFamily(values, help, labels = [label])
                        stat.add_metric([item], '1')
                        print(values,item)
                        yield stat

    def configure(self):
        try:
            print('config_path = ',sys.argv[1])
            config_path = sys.argv[1]
            #config_path = "templates/config.json"
        except Exception as e:
            print(e)
            print('Usage: exporter.py /path/to/config.json')
            sys.exit()
        cfg = open(config_path,'r')
        try:
            config = json.loads(cfg.read())
            cfg.close()
        except:
            cfg.close()
        self.db_name = str(config["connection"]["db_name"])
        self.db_host = str(config["connection"]["db_host"])
        self.db_password = str(config["connection"]["db_password"])
        self.db_user = str(config["connection"]["db_user"])
        self.db_port = int(config["connection"]["db_port"])
        self.metrics = config["metrics"]
        self.db_type = str(config["connection"]["db_type"])


if __name__ == "__main__":
    REGISTRY.register(CustomCollector())
    start_http_server(9118)
    while True:
        time.sleep(1)

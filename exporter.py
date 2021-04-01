from conn.postgres import Postgres
import json
import sys, time
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily


class CustomCollector(object):

    def int_value(self,value):
        none, value = value.split("[(")
        value, none = value.split(",)]")
        return value

    def collect(self):
        self.configure()
        postgres = Postgres(self.db_name,self.db_user,
                self.db_password,self.db_host,self.db_port)
        for metric in self.metrics:
            metric_type = self.metrics[metric]["type"]
            metric_query = self.metrics[metric]["query"]
            metric_datatype = self.metrics[metric]["datatype"]
            print("metric_type == 'gauge'?")
            print(metric_type == 'gauge')
            #print(metric_query)
            print("The metric type is: {0}.".format(metric_type))
            print(type(metric_type))
            if metric_type == 'gauge':
                stat = GaugeMetricFamily(metric, metric, labels=[metric])
                result = str(postgres.read_query(metric_query))
                if metric_datatype == "int":
                    result = self.int_value(result)
                    stat.add_metric('', result)
                if metric_datatype == "str":
                    stat.add_metric(result, '1')
                yield stat
            if metric_type == "counter":
                CounterMetricFamily(metric, metric, labels=[metric])
                result = str(postgres.read_query(metric_query))
                print(result)
                stat.add_metric(result, '')
                yield stat
            #else:
            #    print("Cannot collect metric with metric_type={0}".format(metric_type))
            #    sys.exit()


    def configure(self):
        try:
            #config_path = sys.args(1)
            config_path = "config.json"
        except:
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

        #print(type(self.metrics))
        #print(self.metrics)
        #self.collect()

#collector = CustomCollector()
#collector.configure()
#print(collector.metrics)

if __name__ == "__main__":
    REGISTRY.register(CustomCollector())
    start_http_server(9118)
    while True:
        time.sleep(1)





'''
postgres = Postgres(db_name,db_user,db_password,db_host,db_port)


result = postgres.read_query("select job,name,starttime from public.Job where JobErrors != 0 and JobStatus != 'A' and Name != 'RestoreFiles' and StartTime >= (now() - interval '1 day');")
for item in result:
    print(item)
'''

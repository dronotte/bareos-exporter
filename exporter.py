from conn.postgres import Postgres
import yaml
import sys

db_name = "bareos"
db_user = "exporter"
db_password = "aY78kgvoftQ2sk"
db_host = "192.168.100.104"
db_port = "5432"

try:
    #config_path = sys.args(1)
    config_path = "test.yaml"
except:
    print('Usage: exporter.py /path/to/config.yml')
with open(config_path,'r') as stream:
    config_loaded = yaml.safe_load(stream)
print(config_loaded)





'''
postgres = Postgres(db_name,db_user,db_password,db_host,db_port)


result = postgres.read_query("select job,name,starttime from public.Job where JobErrors != 0 and JobStatus != 'A' and Name != 'RestoreFiles' and StartTime >= (now() - interval '1 day');")
for item in result:
    print(item)
'''

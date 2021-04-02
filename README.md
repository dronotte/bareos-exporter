# Usage:
<br> <br>
## build:
```
docker build -t bareos-exporter .
```
## then:
### docker run:
```
docker run -d -p 9118:9118 -v /opt/bareos-exporter/config.json:/app/config.json -e CONFIG_PATH=/app/config.json --name bareos-exporter bareos-exporter
```
### Or docker-compose:
```
docker-compose up -d
```
## Config example:
```
{
   "connection": {
       "db_type": "postgres",
       "db_name": "bareos",
       "db_host": "192.168.100.104",
       "db_password": "PASSWORD",
       "db_user": "exporter",
       "db_port": 5432
   },
   "metrics": {
     "failed_number": {
        "type": "gauge",
        "datatype": "int",
        "help": "The number of failed jobs",
        "values": "failed_number",
        "label": "job",
        "query": "select count(JobId) as failed_jobs from public.Job where JobErrors != 0 and JobStatus != 'A' and Name != 'RestoreFiles' and StartTime >= (now() - interval '1 day');"
      },
      "failed_names": {
        "type": "gauge",
        "datatype": "str",
        "help": "The names of failed jobs",
        "values": "failed_job",
        "label": "job",
        "query": "select name from public.Job where JobErrors != 0 and JobStatus != 'A' and Name != 'RestoreFiles' and StartTime >= (now() - interval '1 day');"
      }
   }
}
```

Here we describe the parameters for connecting to the Bareos database.
<br>
<br>
We also describe the metrics that we will collect from Bareos. The int data type is normal metrics. The str data type is required to read failed or completed jobs with job titles.
<br> <br>
The output of the second metric in the example in this config will be like this:
```
# HELP failed_job The names of failed jobs
# TYPE failed_job gauge
failed_job{job="backup_bareos_fd"} 1.0
# HELP failed_job The names of failed jobs
# TYPE failed_job gauge
failed_job{job="backup_nginx"} 1.0
# HELP failed_job The names of failed jobs
# TYPE failed_job gauge
failed_job{job="backup_web_app"} 1.0
```

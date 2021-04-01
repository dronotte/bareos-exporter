



Пример конфига:
```
{
   "connection": {
       "db_name": "bareos",
       "db_host": "192.168.100.104",
       "db_password": "aY78kgvoftQ2sk",
       "db_user": "exporter",
       "db_port": 5432
   },
   "metrics": {
     "failed_number": {
        "type": "gauge",
        "datatype": "int",
        "help": "The number of failed jobs",
        "values": "failed_jobs",
        "labels": "",
        "query": "select count(JobId) as failed_jobs from public.Job where JobErrors != 0 and JobStatus != 'A' and Name != 'RestoreFiles' and StartTime >= (now() - interval '1 day');"
      },
      "failed_names": {
        "type": "gauge",
        "datatype": "str",
        "help": "The names of failed job",
        "values": "failed_job",
        "label": "jobs",
        "query": "select name from public.Job where JobErrors != 0 and JobStatus != 'A' and Name != 'RestoreFiles' and StartTime >= (now() - interval '1 day');"
      }
   }
}
```
Здесь мы описываем параметры подключения к базе данных Bareos'а
<br>
<br>
Также описываем метрики, которые будем собирать с Bareos'а. Тип данных int - обычные метрики. Тип данных str необходим для считывания невыполненных или выполненных работ с названиями. <br> <br>
Вывод у второй метрики в этом конфиге будет таким:
```
# HELP backup_failed Failed job backup metric
# TYPE backup_failed gauge
backup_failed{jobs="backup_bareos_fd"} 1.0
# HELP backup_failed Failed job backup metric
# TYPE backup_failed gauge
backup_failed{jobs="backup_dronotte"} 1.0
# HELP backup_failed Failed job backup metric
# TYPE backup_failed gauge
backup_failed{jobs="backup_dronotte"} 1.0
```

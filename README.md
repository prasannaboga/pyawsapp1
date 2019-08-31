# pyawsapp1
This python flask application for aws 


```commandline
docker build -f docker/web/Dockerfile -t pyawsapp1 .
```

```commandline
celery -A celery_tasks.celery worker -l INFO -E --autoscale=100,5 -Q apple  
```


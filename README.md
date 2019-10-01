# pyawsapp1
This python flask application for aws 


```commandline
docker build -f docker/web/Dockerfile -t pyawsapp1 .
docker build -f docker/celery/Dockerfile -t pyawsapp1_celery .
docker build -f docker/redis/Dockerfile -t ecs-redis .
```

```commandline
celery -A celery_tasks.celery worker -l INFO -E --autoscale=5,1 -Q apple,ball,cat 
```


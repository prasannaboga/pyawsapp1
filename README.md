# pyawsapp1
This python flask application for aws 


```commandline
docker build -f docker/web/Dockerfile -t pyawsapp1 .
docker build -f docker/redis/Dockerfile -t ecs-redis .



```
$(aws ecr get-login --no-include-email --region us-east-1 --profile prasanna_awsadmin)

```commandline
celery -A celery_tasks.celery worker -l INFO -E --autoscale=5,1 -Q apple,ball  
```


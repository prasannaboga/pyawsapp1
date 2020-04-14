# Celery Docker File
FROM python:3.6

RUN apt-get update -y

RUN pip3 install pipenv

ENV USER dockeruser
RUN useradd -ms /bin/bash $USER

ENV APP_PATH /home/$USER/my_project
RUN mkdir -p $APP_PATH
COPY . $APP_PATH
WORKDIR $APP_PATH

RUN chown -R $USER:$USER $APP_PATH

RUN pipenv install --system --deploy

USER $USER

CMD celery -A celery_tasks.celery worker -l INFO -E --autoscale=2,1 -Q apple,ball,cat

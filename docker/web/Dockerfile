# Flask Docker File
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

EXPOSE 5000

CMD gunicorn run:my_app -b 0.0.0.0:5000 -w 4

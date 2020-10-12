FROM python:3.9.0-alpine


ENV HOME=/home/app
RUN mkdir $HOME
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . $APP_HOME

RUN mkdir -p $APP_HOME/logs

ENTRYPOINT ["/home/app/web/entrypoint.sh"]
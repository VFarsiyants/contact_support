FROM python:3.12-alpine

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN apk add gcc libc-dev libffi-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./src /code/src
COPY ./alembic /code/alembic
COPY ./main.py /code/main.py
COPY ./alembic.ini /code/alembic.ini
COPY ./docker.env /code/.env
COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN sed -i 's/\r$//g' /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin//docker-entrypoint.sh

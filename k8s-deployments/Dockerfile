FROM python:3.10-buster
ENV PYTHONUNBUFFERED 1

COPY ./dependencies/dev/requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

RUN mkdir /app
WORKDIR /app
COPY . /app

EXPOSE 9000

CMD uwsgi --ini uwsgi.ini

FROM python:3.8

ENV PYTHONBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /mis

COPY requirements.txt /mis

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /mis

CMD ['python', 'manage.py', 'makemigrations']
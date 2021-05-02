# gunicorn-flask

FROM python:3.8

Run mkdir /deploy-app
COPY . /deploy-app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]

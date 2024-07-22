FROM python:3.10.12
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./app ./app

RUN python3 ./app/manage.py makemigrations
RUN python3 ./app/manage.py migrate

CMD [ "python3", "./app/manage.py", "runserver", "0.0.0.0:8000"]

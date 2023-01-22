FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-tk -y
RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

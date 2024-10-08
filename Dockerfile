FROM python:3.12.6-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get -y install openssh-server \
    && pip install -r requirements.txt
#CMD ["python", "./main.py"]
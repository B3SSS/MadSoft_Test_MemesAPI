FROM python:3.9-slim

COPY requirements.txt reqs.txt
RUN pip install -r reqs.txt

COPY . /app
WORKDIR /app
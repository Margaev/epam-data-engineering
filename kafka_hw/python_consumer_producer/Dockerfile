FROM python:latest
RUN apt-get install gcc
COPY . .
RUN pip install -r requirements.txt
CMD bash add_postgres_connector.sh && bash add_es_connector.sh && python3 consumer_producer.py
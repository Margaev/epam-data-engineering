FROM python:latest
RUN apt-get install gcc
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "populate_postgres_table.py"]
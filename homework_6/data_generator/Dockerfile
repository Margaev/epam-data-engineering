FROM python:latest
RUN apt-get install gcc
#COPY requirements.txt requirements.txt
COPY . .
RUN pip install -r requirements.txt
#COPY populate_postgres_table.py populate_postgres_table.py
CMD ["python3", "populate_postgres_table.py"]
FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt /requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY .env /.env
COPY process_files.py /process_files.py
CMD ["sh", "-c", "flask run -h 0.0.0.0 -p $FLASK_PORT"]

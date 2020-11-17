from flask import Flask, request, jsonify
from dotenv import load_dotenv
import gzip
from tempfile import TemporaryFile
from collections import defaultdict

load_dotenv('.env')

app = Flask(__name__)


def read_in_chunks(file):
    while True:
        data = file.read(int(1e+9))
        if not data:
            break
        yield data


@app.route('/', methods=['POST'])
def sum_bytes():
    bytes_counts = defaultdict(int)

    # Для каждого файла в request.files создать временный файл, распаковать его
    # и добавить в ответ в формате <имя файла>: <количество ненулевых байтов>
    for filename, file in request.files.items():
        temp = TemporaryFile()
        temp.write(file.read())
        temp.seek(0)

        with gzip.GzipFile(mode='rb', fileobj=temp) as f:
            for chunk in read_in_chunks(f):
                not_null_bytes = list(filter(lambda x: x != 0, chunk))
                bytes_counts[filename] += len(not_null_bytes)

    # Вернуть ответ в формате json
    return jsonify(bytes_counts)

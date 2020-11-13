from flask import Flask, request, jsonify
from dotenv import load_dotenv
import gzip
from tempfile import NamedTemporaryFile
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
    sums_of_bytes = defaultdict(int)

    # Для каждого файла в request.files создать временный файл, распаковать его
    # и добавить в ответ в формате <имя файла>: <сумма ненулевых байтов>
    for filename, file in request.files.items():
        temp = NamedTemporaryFile()
        temp.write(file.read())

        with gzip.open(temp.name, 'rb') as f:
            for chunk in read_in_chunks(f):
                sums_of_bytes[filename] += sum(chunk)

    # Вернуть ответ в формате json
    return jsonify(sums_of_bytes)

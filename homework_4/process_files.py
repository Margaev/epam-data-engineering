from flask import Flask, request, jsonify
from dotenv import load_dotenv
import gzip
from tempfile import NamedTemporaryFile

load_dotenv('.env')

app = Flask(__name__)


@app.route('/', methods=['POST'])
def sum_bytes():
    sums_of_bytes = {}

    # Для каждого файла в request.files создать временный файл, распаковать его
    # и добавить в ответ в формате <имя файла>: <сумма ненулевых байтов>
    for filename, file in request.files.items():
        temp = NamedTemporaryFile()
        temp.write(file.read())

        with gzip.open(temp.name, 'rb') as f:
            sums_of_bytes[filename] = sum(f.read())

    # Вернуть ответ в формате json
    return jsonify(sums_of_bytes)

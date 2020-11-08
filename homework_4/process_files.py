from flask import Flask, request, jsonify
from dotenv import load_dotenv
import gzip
from tempfile import NamedTemporaryFile

load_dotenv('.env')

app = Flask(__name__)


@app.route('/', methods=['POST'])
def sum_bytes():
    sums_of_bytes = {}

    for filename, file in request.files.items():
        temp = NamedTemporaryFile()
        temp.write(file.read())

        with gzip.open(temp.name, 'rb') as f:
            sums_of_bytes[filename] = sum(f.read())

    return jsonify(sums_of_bytes)

from queue import Queue
from sys import argv
import os
from collections import defaultdict
import grequests

from settings import STARTING_PORT, NUM_OF_CONTAINERS

failed_tasks = defaultdict(list)


def get_files_queue(directory_name):
    # Возвращает очередь из файлов в директории directory_name
    file_list = os.listdir(directory_name)
    q = Queue()
    for file in file_list:
        q.put(file)

    return q


def get_urls():
    # Возвращает список адресов контейнеров
    urls = []

    for i in range(NUM_OF_CONTAINERS):
        urls.append(f'http://localhost:{STARTING_PORT + i}/')

    return urls


def distribute_files(files_queue, data_directory, urls):
    # Возвращает список запросов, которые нужно послать асинхронно на каждый контейнер
    rs = []

    for i in range(NUM_OF_CONTAINERS):
        # Если в очереди ещё есть файлы, добавить новый запрос
        if not files_queue.empty():
            file = files_queue.get()
            files = {file: open(os.path.abspath(os.path.join(data_directory, file)), 'rb')}

            url = urls[i]
            rs.append(grequests.post(url, files=files))

    return rs


def reduce_results(responses):
    # Складывает ответы всех запросов с кодом 200 и возвращает сумму
    result = 0
    for r in responses:
        if r is not None and r.ok:
            for i, s in r.json().items():
                result += s

    return result


def exception_handler(request, exception):
    # Обработка исключений при отправке запросов на контейнеры
    failed_tasks[request.url].extend(request.kwargs['files'].keys())


def main():
    if len(argv) != 2:
        print(f'usage: {argv[0]} <input data directory>')
        exit(1)

    data_directory = argv[1]
    files_queue = get_files_queue(data_directory)
    urls = get_urls()
    responses = []

    while not files_queue.empty():
        rs = distribute_files(files_queue, data_directory, urls)
        current_batch_responses = grequests.map(rs, exception_handler=exception_handler)
        responses.extend(current_batch_responses)

    result = reduce_results(responses)

    print('result:', result)
    print('responses:', responses)
    print('errors:', dict(failed_tasks))


if __name__ == '__main__':
    main()

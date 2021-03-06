Установка:

1) Добавить текущего юзера в группу docker:

    `sudo gpasswd -a $USER docker`

2) Либо создать нового юзера и добавить его в группу docker:

    `sudo useradd <username>`
    
    `sudo gpasswd -a <username> docker`
    
    `su <username>`

3) Создать файл .env по шаблону template.txt

4) Собрать docker image:

    `docker build --tag map_reduce_docker .`
    
5) Создать virtual environment:

    `python3 -m venv venv`

6) Установить зависимости:

    `pip3 install -r requirements.txt`
    
7) Запустить контейнеры:

    `python3 run_containers.py`
    
    Если хотите прекратить работу нажмите `ctrl + C` и дождитесь остановки контейнеров
    
8) Запустить задачу для контейнеров:

    `python3 start_job.py <path to data directory>`
    
    result - сумма ненулевых байт в файлах
    
    responses - ответы контейнеров на запросы на запуск задач
    
    errors - ошибки в формате {<ссылка на сервер> : <имя файла>}
    
    
Описание:

На каждом из контейнеров крутится небольшой скрипт на Flask (process_files.py), который ожидает запросов с архивами
в теле и подсчитывает сумму ненулевых байт заархивированного файла.
Каждый скрипт запускается на отдельном порту начиная с STARTING_PORT и заканчивая STARTING_PORT + NUM_OF_CONTAINERS из .env.
Такое решение можно запустить с минимальными изменениями не только на docker контейнерах но и на разных машинах, объединённых в сеть.

Скрипт run_containers.py запускает N контейнеров и ждёт комбинации клавиш `ctrl + C` для окончания работы.

Скрипт start_job.py создаёт очередь из файлов и асинхронно посылает по одному файлу на каждую машину, затем, дождавшись
ответа, суммирует все суммы байтов отдельных файлов и выводит ответ. Так же ведётся отслеживание ошибок выполнения на
контейнерах и они выводятся в формате {<ссылка на сервер> : <имя файла>}.
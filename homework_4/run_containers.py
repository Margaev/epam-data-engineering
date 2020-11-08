import sys
import docker
import signal

from settings import IMAGE_NAME, STARTING_PORT, NUM_OF_CONTAINERS

containers = []


def run_containers(client, n):
    # Запустить n контейнеров, на последовательности портов,
    # начиная с STARTING_PORT и заканчивая STARTING_PORT + NUM_OF_CONTAINERS
    for i in range(n):
        port = STARTING_PORT + i
        env = {
            'FLASK_PORT': port
        }

        c = client.containers.run(
            image=IMAGE_NAME,
            ports={f'{port}/tcp': port},
            environment=env,
            detach=True
         )

        print(f'Running container with id {c.id}')

        containers.append(c)


def signal_handler(sig, frame):
    # Обработка ctrl + C, остановка всех запущенных контейнеров
    print('\nStopping containers')
    for c in containers:
        print(f'Stopping container with id {c.id}')
        c.stop()

    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    client = docker.from_env()
    run_containers(client, NUM_OF_CONTAINERS)

    # Ожидание сочетания клавиш ctrl + C
    signal.pause()


if __name__ == '__main__':
    main()

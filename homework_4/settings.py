import os
from dotenv import load_dotenv

IMAGE_NAME = 'map_reduce_docker'
load_dotenv('.env')
try:
    NUM_OF_CONTAINERS = os.environ['NUM_OF_CONTAINERS']
    NUM_OF_CONTAINERS = int(NUM_OF_CONTAINERS)

    if NUM_OF_CONTAINERS <= 0:
        print('NUM_OF_CONTAINERS must be positive integer')
        exit(1)

    STARTING_PORT = os.environ['STARTING_PORT']
    STARTING_PORT = int(STARTING_PORT)

    if STARTING_PORT <= 0:
        print('STARTING_PORT must be positive integer')
        exit(1)
except KeyError:
    print('You need to add this to your .env file: MOUNT_DIR=<path to mount point for docker>')
    print('You need to add this to your .env file: NUM_OF_CONTAINERS=<number of containers>')
    exit(1)
except ValueError:
    print('NUM_OF_CONTAINERS and STARTING_PORT must be positive integers')
    exit(1)
import filecmp
from collections import defaultdict
import os
from os.path import isfile, join, abspath
from sys import argv


def get_duplicates(path):
    duplicates = defaultdict(list)
    file_list = [abspath(join(path, f)) for f in os.listdir(path) if isfile(join(path, f))]
    checked = set()

    for file in file_list:
        checked.add(file)
        for other_file in filter(lambda x: x not in checked, file_list):
            if filecmp.cmp(file, other_file):
                duplicates[file].append(other_file)
                checked.add(other_file)

    return duplicates


def replace_duplicates(duplicates):
    for file, file_duplicates in duplicates.items():
        for duplicate in file_duplicates:
            os.remove(duplicate)
            os.system(f'ln {file} {duplicate}')


def main():
    path = argv[1]
    duplicates = get_duplicates(path)
    replace_duplicates(duplicates)


if __name__ == '__main__':
    main()

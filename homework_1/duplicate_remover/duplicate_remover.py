#!/usr/bin/env python3
import filecmp
from collections import defaultdict
import os
from os.path import join, abspath
from sys import argv


def get_duplicates(path):
    """
    Returns dict with keys as files and value as a list of their duplicates
    """
    duplicates = defaultdict(list)
    # collect all files with absolute path in given directory (including subdirectories)
    file_list = [abspath(join(dir_name, f)) for dir_name, _, files in os.walk(path) for f in files]
    checked = set()

    # Iterating through the file list skipping over already checked files
    for file in file_list:
        checked.add(file)
        for other_file in filter(lambda x: x not in checked, file_list):
            if filecmp.cmp(file, other_file):
                duplicates[file].append(other_file)
                checked.add(other_file)

    return duplicates


def replace_duplicates(duplicates):
    """
    Replaces all duplicates with hard links
    """
    for file, file_duplicates in duplicates.items():
        for duplicate in file_duplicates:
            os.remove(duplicate)
            os.link(file, duplicate)


def main():
    if len(argv) != 2:
        print(f'usage: {argv[0]} <path>')
        exit(1)

    path = argv[1]
    duplicates = get_duplicates(path)
    replace_duplicates(duplicates)


if __name__ == '__main__':
    main()

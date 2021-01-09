#!/usr/bin/env python3
from collections import defaultdict
import os
from os.path import join, abspath
from sys import argv
import binascii


def get_duplicates(path):
    """
    Returns dict with keys as files and value as a list of their duplicates
    """
    # Collect all files with absolute path in given directory (including subdirectories)
    file_list = [abspath(join(dir_name, f)) for dir_name, _, files in os.walk(path) for f in files]

    duplicates = defaultdict(list)
    file_hashes = dict()

    for file in file_list:
        with open(file, 'rb') as f:
            # For every file calculate hash from its content
            file_hash = binascii.crc32(f.read())
            # If file not in file_hashes, write to it file_hash: filename
            if file_hash not in file_hashes:
                file_hashes[file_hash] = file
            # If file in file_hashes, append it to result duplicates dict
            else:
                duplicates[file_hashes[file_hash]].append(file)

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

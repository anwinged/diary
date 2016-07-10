#!/usr/bin/python
# coding: utf-8

import datetime
import os
import subprocess
import sys


ROOR_DIRECTORY_ENV = 'DIARY_ROOT_DIRECTORY'

ROOT_DIRECTORY_DEFAULT = '/home/av/Dropbox/Diary'


def main():
    root_directory = get_root_directory()
    check_root_directory(root_directory)
    filename = get_file_name()
    full_path = os.path.join(root_directory, filename)
    touch_file(full_path)
    run_editor(full_path)


def get_root_directory():
    return os.getenv(ROOR_DIRECTORY_ENV, ROOT_DIRECTORY_DEFAULT)


def check_root_directory(root_directory):
    if not os.path.exists(root_directory):
        print 'Root directory "{}" does not exists'.format(root_directory)
        sys.exit(1)


def get_file_name():
    today = datetime.date.today()
    return '{:04}-{:02}-{:02}.md'.format(today.year, today.month, today.day)


def get_template():
    template = [
        '---',
        'Title: Запись {day}.{month}.{year}',
        '---',
        '',
        '',
    ]
    today = datetime.date.today()
    return '\n'.join(template).format(**{
        'day': today.day,
        'month': today.month,
        'year': today.year,
    })


def touch_file(full_path):
    if os.path.exists(full_path):
        return

    template = get_template()
    with open(full_path, 'w') as new_file:
        new_file.write(template)


def run_editor(full_path):
    subprocess.Popen(['subl', full_path])


if __name__ == '__main__':
    main()

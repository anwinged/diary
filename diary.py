#!/usr/bin/python
# coding: utf-8

import datetime
import os
import subprocess
import sys


ROOR_DIRECTORY_ENV = 'DIARY_ROOT_DIRECTORY'

EDITOR_ENV = 'DIARY_EDITOR'

EDITOR_VARIABLES = [
    EDITOR_ENV,
    'VISUAL',
    'EDITOR',
]

DEFAULT_EDITOR = 'vi'


def main():
    root_directory = get_root_directory()
    check_root_directory(root_directory)
    editor = get_editor()
    check_editor(editor)
    filename = get_file_name()
    full_path = os.path.join(root_directory, filename)
    touch_file(full_path)
    run_editor(editor, full_path)


def get_root_directory():
    return os.getenv(ROOR_DIRECTORY_ENV)


def check_root_directory(root_directory):
    if root_directory is None:
        print 'Root directory not setup. Use {} environment variable'.format(ROOR_DIRECTORY_ENV)
        sys.exit(1)

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


def get_editor():
    editors = [os.getenv(i) for i in EDITOR_VARIABLES]
    available = [editor for editor in editors if editor]
    return next(iter(available), DEFAULT_EDITOR)


def check_editor(editor):
    if editor is None:
        list_of_variables = ', '.join(EDITOR_VARIABLES)
        print 'Editor not found. Check environment variables: {}'.format(list_of_variables)
        sys.exit(1)


def run_editor(editor, full_path):
    subprocess.call([editor, full_path])


if __name__ == '__main__':
    main()

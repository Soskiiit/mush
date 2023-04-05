#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess as sp
import argparse


class static_property:
    def __init__(self, getter, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.getter = getter
    def __get__(self, obj, objtype):
        return self.getter(*self.args, **self.kwargs)
    @staticmethod
    def __call__(cls, *args, **kwargs):
        return static_property(cls, *args, **kwargs)


class Settings:
    @static_property
    def PROJECT_NAME():
        return 'mush'

    @static_property
    def ROOT_DIR():
        return os.path.realpath(os.path.dirname(__file__))

    @static_property
    def PROJECT_DIR():
        return os.path.join(Settings.ROOT_DIR, Settings.PROJECT_NAME)

    @static_property
    def VENV_DIR():
        return os.path.join(Settings.ROOT_DIR, '.venv')


def _run_command(
        cmd: str, 
        cwd: str=Settings.PROJECT_DIR,
        title: str=None, 
        verbose=False) -> bool:
    try:
        if title is not None:
            print(f'----- {title} -----')
        if verbose:
            print(f'> {cmd}')
        sp.check_call(cmd, cwd=cwd, shell=True)
    except Exception as e:
        print(str(e))
        return False

    return True


def main():
    arg_parser = argparse.ArgumentParser(
        description='Manage this project with just a few commands'
    )
    arg_parser.add_argument(
        '-s', '--setup',
        dest='setup',
        action='store_true',
        help='Create virtual environment, install dependencies, ' +
        'set up pre-commit, create .env, migrate database and add admin user'
    )
    arg_parser.add_argument(
        '-r', '--run',
        dest='run',
        action='store_true',
        help='Run development server'
    )
    arg_parser.add_argument(
        '-t', '--test',
        dest='test',
        action='store_true',
        help='Run Django tests'
    )
    arg_parser.add_argument(
        '-l', '--lint',
        dest='lint',
        action='store_true',
        help='Run linters'
    )
    args = arg_parser.parse_args()

    if len(sys.argv) == 1:
        arg_parser.print_help()
        quit()

    print('Nothing to do right now.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()

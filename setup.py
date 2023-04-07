#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess as sp


PROJECT_NAME            = 'mush'
ROOT_DIR                = os.path.realpath(os.path.dirname(__file__))
PROJECT_DIR             = os.path.join(ROOT_DIR, PROJECT_NAME)
VENV_DIR                = os.path.join(ROOT_DIR, '.venv')
VENV_PYTHON             = os.path.join(VENV_DIR, 'bin', 'python3') if sys.platform == 'linux' else os.path.join(VENV_DIR, 'Scripts', 'python.exe')
VENV_PRECOMMIT          = os.path.join(VENV_DIR, 'bin', 'pre-commit')
MANAGEPY_PATH           = os.path.join(PROJECT_DIR, 'manage.py')
DEV_REQUIREMENTS_PATH   = os.path.join(ROOT_DIR, 'requirements', 'dev.txt')
DOTENV_PATH             = os.path.join(PROJECT_DIR, '.env')
DOTENV_CONTENTS = {
    'DJANGO_DEBUG': True,
    'DJANGO_SECRET_KEY': 'secret_key',
    'DJANGO_ALLOWED_HOSTS': 'localhost,127.0.0.1',
    'DJANGO_INTERNAL_IPS': 'localhost,127.0.0.1',
}


def run(cmd: list, stdout=sp.PIPE, stderr=sp.PIPE, ignore_errors=False, *args, **kwargs):
    print('>', ' '.join(cmd))
    r = sp.run(cmd, stdout=stdout, stderr=stderr, *args, **kwargs)
    if r.returncode != 0 and not ignore_errors:
        print(r.stdout.decode(), r.stderr.decode(), sep='\n')
        quit()


def setup():
    if sys.prefix == sys.base_prefix:
        shutil.rmtree(VENV_DIR, ignore_errors=True)
        run(['python', '-m', 'venv', VENV_DIR])
        run([VENV_PYTHON, __file__] + sys.argv[1:], stdout=None, stderr=None)
        exit(0)

    run([sys.executable, '-m', 'pip', 'install', '-r', DEV_REQUIREMENTS_PATH])
    run([sys.executable, MANAGEPY_PATH, 'migrate'])
    run([sys.executable, MANAGEPY_PATH, 'shell'], input=b'from django.contrib.auth.models import User; User.objects.create_superuser("admin", "admin@mail.com", "admin")\n', stdout=sp.DEVNULL, stderr=sp.DEVNULL, ignore_errors=True)

    run([VENV_PRECOMMIT, 'install', '--hook-type', 'pre-commit'])
    run([VENV_PRECOMMIT, 'install', '--hook-type', 'pre-push'])
    run([VENV_PRECOMMIT, 'install', '--install-hooks'])
    with open(DOTENV_PATH, 'w') as file:
        file.write('\n'.join(f'{k}={v}' for k,v in DOTENV_CONTENTS.items()))


if __name__ == '__main__':
    try:
        setup()
    except KeyboardInterrupt:
        print()

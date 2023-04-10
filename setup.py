#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess as sp
import urllib.request
import tempfile


PROJECT_NAME            = 'mush'
ROOT_DIR                = os.path.realpath(os.path.dirname(__file__))
PROJECT_DIR             = os.path.join(ROOT_DIR, PROJECT_NAME)
VENV_DIR                = os.path.join(ROOT_DIR, '.venv')
VENV_PYTHON             = os.path.join(VENV_DIR, 'bin', 'python3') if sys.platform in ['linux', 'darwin'] else os.path.join(VENV_DIR, 'Scripts', 'python.exe')
VENV_PRECOMMIT          = os.path.join(VENV_DIR, 'bin', 'pre-commit')
REQUIREMENTS_PATH       = os.path.join(ROOT_DIR, 'requirements', 'dev.txt')
MANAGEPY_PATH           = os.path.join(PROJECT_DIR, 'manage.py')
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


def setup_venv():
    if sys.prefix == sys.base_prefix:
        print('Setting up virtual environment...')
        shutil.rmtree(VENV_DIR, ignore_errors=True)
        run(['python', '-m', 'venv', VENV_DIR])
        run([VENV_PYTHON, __file__] + sys.argv[1:], stdout=None, stderr=None)
        exit(0)


def setup():
    print('Setting up the project...')
    run([sys.executable, '-m', 'pip', 'install', '-r', REQUIREMENTS_PATH])
    run([sys.executable, MANAGEPY_PATH, 'migrate'])
    run([sys.executable, MANAGEPY_PATH, 'shell'], input=b'from django.contrib.auth.models import User; User.objects.create_superuser("admin", "admin@mail.com", "admin")\n', stdout=sp.DEVNULL, stderr=sp.DEVNULL, ignore_errors=True)

    run([VENV_PRECOMMIT, 'install', '--hook-type', 'pre-commit'])
    run([VENV_PRECOMMIT, 'install', '--hook-type', 'pre-push'])
    run([VENV_PRECOMMIT, 'install', '--install-hooks'])
    with open(DOTENV_PATH, 'w') as file:
        file.write('\n'.join(f'{k}={v}' for k,v in DOTENV_CONTENTS.items()))


def install_metashape():
    base_url = 'https://s3-eu-west-1.amazonaws.com/download.agisoft.com/'
    metashape_packages = {
        'linux': 'Metashape-2.0.1-cp37.cp38.cp39.cp310.cp311-abi3-linux_x86_64.whl',
        'darwin': 'Metashape-2.0.1-cp37.cp38.cp39.cp310.cp311-abi3-macosx_11_0_universal2.macosx_10_13_x86_64.whl',
        'windows': 'Metashape-2.0.1-cp37.cp38.cp39.cp310.cp311-none-win_amd64.whl',
    }

    print('Installing Metashape package...')
    with tempfile.TemporaryDirectory() as temp_dir:
        package_name = metashape_packages[sys.platform]
        package_path = os.path.join(temp_dir, package_name)

        print('Downloading...')
        with open(package_path, 'wb') as file:
            with urllib.request.urlopen(base_url + package_name) as resp:
                file.write(resp.read())

        print('Installing...')
        run([sys.executable, '-m', 'pip', 'install', package_path])


if __name__ == '__main__':
    try:
        setup_venv()
        install_metashape()
        setup()
    except KeyboardInterrupt:
        print()

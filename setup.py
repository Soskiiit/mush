#!/usr/bin/env python3

import os
import platform
import sys
import shutil
import subprocess as sp


PROJECT_NAME            = 'mush'
ROOT_DIR                = os.path.realpath(os.path.dirname(__file__))
PROJECT_DIR             = os.path.join(ROOT_DIR, PROJECT_NAME)
VENV_DIR                = os.path.dirname(os.path.dirname(os.path.dirname(sys.path[-1])))
VENV_PYTHON             = os.path.join(VENV_DIR, 'bin', 'python3') if sys.platform == 'linux' else os.path.join(VENV_DIR, 'Scripts', 'python.exe')
VENV_PRECOMMIT          = os.path.join(VENV_DIR, 'bin', 'pre-commit')
MANAGEPY_PATH           = os.path.join(PROJECT_DIR, 'manage.py')
DEV_REQUIREMENTS_PATH   = os.path.join(ROOT_DIR, 'requirements', 'dev.txt')
DOTENV_PATH             = os.path.join(PROJECT_DIR, '.env')
METASHAPE_DOWNLOAD_LINKS = {
    'Windows': 'https://s3-eu-west-1.amazonaws.com/download.agisoft.com/Metashape-2.0.1-cp37.cp38.cp39.cp310.cp311-none-win_amd64.whl',
    'Linux': 'https://s3-eu-west-1.amazonaws.com/download.agisoft.com/Metashape-2.0.1-cp37.cp38.cp39.cp310.cp311-abi3-linux_x86_64.whl',
    'Darwin': 'https://s3-eu-west-1.amazonaws.com/download.agisoft.com/Metashape-2.0.1-cp37.cp38.cp39.cp310.cp311-abi3-macosx_11_0_universal2.macosx_10_13_x86_64.whl'
}
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


def install_metashape_package():
    system = platform.system()
    if system in METASHAPE_DOWNLOAD_LINKS:
        os.system(f'python3 -m pip install {METASHAPE_DOWNLOAD_LINKS[system]}')
    else:
        print('Photogrammetry support on your system isn`t avaliable')


def setup():
    if sys.prefix == sys.base_prefix:
        shutil.rmtree(VENV_DIR, ignore_errors=True)
        run(['python', '-m', 'venv', VENV_DIR])
        run([VENV_PYTHON, __file__] + sys.argv[1:], stdout=None, stderr=None)
        exit(0)

    run([sys.executable, '-m', 'pip', 'install', '-r', DEV_REQUIREMENTS_PATH])
    install_metashape_package()
    run([sys.executable, MANAGEPY_PATH, 'migrate'])
    run([sys.executable, MANAGEPY_PATH, 'shell'], input=b'from users.models import User; User.objects.create_superuser("admin", "admin@mail.com", "admin")\n', stdout=sp.DEVNULL, stderr=sp.DEVNULL, ignore_errors=True)
    try:
        run([VENV_PRECOMMIT, 'install', '--hook-type', 'pre-commit'])
        run([VENV_PRECOMMIT, 'install', '--hook-type', 'pre-push'])
        run([VENV_PRECOMMIT, 'install', '--install-hooks'])
    except FileNotFoundError:
        print('can`t initialize hooks')
    with open(DOTENV_PATH, 'w') as file:
        file.write('\n'.join(f'{k}={v}' for k,v in DOTENV_CONTENTS.items()))
    print('All done. Super user credentials are "admin:admin"')


if __name__ == '__main__':
    try:
        setup()
    except KeyboardInterrupt:
        print()

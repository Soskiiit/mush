# Mush3D

**Useful links:**
- [ExcaliDraw Board](https://excalidraw.com/#room=40d1ff70b3686a5c5b03,w6kdCY5a6fkLumdioki-Cg)

## Installing
**Clone the repository**
```
git clone https://github.com/Soskiiit/mush.git
cd mush
```

**Set up virtual environment**
```
python -m venv .venv
```
And activate it.

**Install the dependencies**
- production: `pip install -r requirements/main.txt`
- dev: `pip install -r requirements/dev.txt`

**Managing `.env` file:**
1. Create `.env` file inside `django_project/` folder:
2. Define these settings:
  - `DJANGO_DEBUG` - `True`/`False`.
  - `DJANGO_ALLOWED_HOSTS` - comma-separeted list of allowed hosts.
  - `DJANGO_INTERNAL_IPS` - comma-separeted list of IPs under which `debug_toolbar` would be shown.
  - `DJANGO_SECRET_KEY` - Generate secret key. You can use this command: `python -c 'from django.core.management.utils import get_random_secret_key as grsk; print(grsk())'`.

Example `.env` may look like this:
```
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=secret_key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_INTERNAL_IPS=localhost,127.0.0.1
```

**Running linters and Django tests**
1. Install `dev` dependencies with `pip install -r requirements/dev.txt` command.
2. Install pre-commit git hooks:
  - `pre-commit install --hook-type pre-commit`
  - `pre-commit install --hook-type pre-push`

- *Linters* now will run on every **commit**. Type `pre-commit run -a` to run them manually.
- *Tests* will run on every **push** or on `pre-commit run --hook-stage manual tests` command.

## Compiling localization messages
```
python ./mush/manage.py makemessages -a
python ./mush/manage.py compilemessages --ignore .venv
```

## Running development server
```
python ./mush/manage.py runserver
```

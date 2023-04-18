# Mush3D

[![Code Quality Check](https://github.com/Soskiiit/mush/actions/workflows/linters.yml/badge.svg)](https://github.com/Soskiiit/mush/actions/workflows/linters.yml) [![Django Tests](https://github.com/Soskiiit/mush/actions/workflows/tests.yml/badge.svg)](https://github.com/Soskiiit/mush/actions/workflows/tests.yml)

**Useful links:**
- [ToDo list](todo.md)
- [ExcaliDraw Board](https://excalidraw.com/#room=40d1ff70b3686a5c5b03,w6kdCY5a6fkLumdioki-Cg)

## Installing

**Clone the repository**

```
git clone https://github.com/Soskiiit/mush.git
cd mush
```

**Setting up the project**

```
python setup.py
```

**Installing photogrammetry engine**

1. Download Metashape python package and start free trial
   https://agisoft.freshdesk.com/support/solutions/articles/31000148930-how-to-install-metashape-stand-alone-python-module
2. Install package using pip

```
pip install ...Metashape-...whl
```

**Running linters and Django tests**

- *Linters* will run on every **commit**. Type `pre-commit run -a` to run them manually.
- *Tests* will run on every **push** or with `pre-commit run --hook-stage manual tests` command.

You can always skip pre-commit hooks when committing changes by adding `--no-verify` flag.

## Compiling localization messages

```
python ./mush/manage.py makemessages -a
python ./mush/manage.py compilemessages --ignore .venv
```

## Dumping fixtures
```
./mush/manage.py dumpdata --natural-foreign --natural-primary users  &> ./mush/users/fixtures/default.json
./mush/manage.py dumpdata --natural-foreign --natural-primary catalog &> ./mush/catalog/fixtures/default.json
```

## Running development server

```
python ./mush/manage.py runserver
```

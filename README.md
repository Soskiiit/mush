# Mush3D

[![Code Quality Check](https://github.com/Soskiiit/mush/actions/workflows/linters.yml/badge.svg)](https://github.com/Soskiiit/mush/actions/workflows/linters.yml) [![Django Tests](https://github.com/Soskiiit/mush/actions/workflows/tests.yml/badge.svg)](https://github.com/Soskiiit/mush/actions/workflows/tests.yml)

**Useful links:**
- [ExcaliDraw Board](https://excalidraw.com/#room=40d1ff70b3686a5c5b03,w6kdCY5a6fkLumdioki-Cg)

## Installing

**Clone the repository**

```
git clone https://github.com/Soskiiit/mush.git
cd mush
```

**Creating the virtual environment**

```
python3 -m venv venv
```

**How to activate virtual environment**

***Windows***
```
venv\Scripts\activate
```

***Linux***
```
source ./venv/bin/activate
```

**Setting up the project**

```
python3 setup.py
```

**Installing photogrammetry engine**

1. Download [Metashape professional edition](https://www.agisoft.com/downloads/installer/) and install it

2. Activate your license or start free trial

## Running development server

1. Run server with
```
python3 ./manage.py
```
2. If you want to use photogrammetry run worker with
```
python3 ./photogrammetry/photogrammetry_processor.py
```

**Running linters and Django tests**

- *Linters* will run on every **commit**. Type `pre-commit run -a` to run them manually.
- *Tests* will run on every **push** or with `pre-commit run --hook-stage manual tests` command.

You can always skip pre-commit hooks when committing changes by adding `--no-verify` flag.

## Dumping fixtures
```
./mush/manage.py dumpdata --natural-foreign --natural-primary users  &> ./mush/users/fixtures/default.json
./mush/manage.py dumpdata --natural-foreign --natural-primary catalog &> ./mush/catalog/fixtures/default.json
```

## Running development server

```
python3 ./mush/manage.py runserver
```

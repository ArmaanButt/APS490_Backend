# Requirements

- `python 3.4.3`
- `pyvenv`
- MYSQL server
- Docker

# Setup

- `pyvenv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

# Running the app

## Locally

- Activate venv
- `python run.py`

## Inside docker container

- `docker-compose up -d`

# Running the tests

- `nosetests -v`

# New Endpoint

- `add_resource`
- DB Model
- Resource contract, Params contract
- Collection, detail class
- Tests
- DB migration

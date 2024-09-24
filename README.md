# BigId home task

This project is a home task for BigId involving an api and a databse

## Installation

Use the package manager [poetry](https://python-poetry.org/docs/) to install. \
Needed only for running locally.

```bash 
poetry install
```

## Running

### Locally

Running is done with poetry. \
make sure you have a .env file like in the repo to run properly.

```bash
docker run -p 6379:6379 redis:7
celery -A app.text_proccesors.most_common_word.celery worker --loglevel=info
poetry run python -m app.main
```

### With docker-compose
Make sure you have the docker-compose.yaml to run. \
Note that a second env file named .env.docker-network \
that is needed to override some variables for the containers to work properly.
```bash
docker-compose up
```

## Data
The data that the applicatiopn currently produces is a .log file and \
the bigid.db that is used by sqlite. They are both saved in \
./persistent_data folder
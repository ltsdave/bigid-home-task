# BigId home task

This project is a home task for BigId involving an api and a databse

## Installation

Use the package manager [poetry](https://python-poetry.org/docs/) to install.

```bash 
poetry install
```

## Running the compnents

Running is also done with poetry.

```bash
docker run -p 6379:6379 redis:7
celery -A app.text_proccesors.most_common_word.celery worker --loglevel=info
poetry run python -m app.main
```

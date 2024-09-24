FROM python:3.12-slim

# Set environment variables
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install Poetry
RUN pip install poetry

WORKDIR /BigId
COPY pyproject.toml poetry.lock /BigId/
RUN poetry install --no-root
COPY . /BigId
EXPOSE 8000
CMD ["poetry", "run", "python", "-m", "app.main"]
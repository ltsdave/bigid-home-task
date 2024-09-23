FROM python:3.12-slim
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root
COPY . /app
EXPOSE 8000
CMD ["poetry", "run", "python", "-m", "app.main"]

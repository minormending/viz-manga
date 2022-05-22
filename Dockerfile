FROM python:3.10-slim

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN mkdir -p /app/viz_manga
COPY pyproject.toml /app
COPY README.md /app
COPY viz_manga /app/viz_manga

WORKDIR /app
RUN poetry install --no-dev

ENTRYPOINT [ "viz-manga-cli" ]
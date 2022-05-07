FROM python:3.10

RUN mkdir /app
COPY pyproject.toml /app 
WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY viz_manga /app
ENTRYPOINT [ "python", "./manga.py" ]
FROM python:3.11

WORKDIR /usr/src/app

RUN pip install "poetry==1.3.2" \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /usr/src/app/

RUN poetry install --only main --no-interaction --no-ansi -vvv

COPY . .

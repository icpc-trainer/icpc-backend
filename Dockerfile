FROM python:3.11

LABEL maintainer="peskovdev@proton.me"

WORKDIR /code

RUN pip install poetry

RUN apt-get update \
  && apt-get install -y netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock /code/

RUN poetry config virtualenvs.create false \
  && poetry install --only main

COPY . /code/

RUN poetry install --only main

ENTRYPOINT ["/code/boot.sh"]

FROM python:3.8-slim-buster as base
WORKDIR /app

RUN pip install poetry \
  && poetry config virtualenvs.create false

FROM base as production
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-dev
COPY . /app

CMD gunicorn --bind 0.0.0.0:${PORT:-5000} wsgi:app

FROM base as development
COPY poetry.lock pyproject.toml /app/
RUN poetry install
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

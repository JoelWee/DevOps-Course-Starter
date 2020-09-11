FROM python:3.8-slim-buster as base


FROM base as production
WORKDIR /app

RUN pip install poetry \
  && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-dev

COPY . /app

EXPOSE 5000
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT ["poetry", "run", "gunicorn", "-c", "./gunicorn.conf.py", "wsgi:app"]

FROM base as development
WORKDIR /app

RUN pip install poetry \
  && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/
RUN poetry install
EXPOSE 5000
ENTRYPOINT ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]

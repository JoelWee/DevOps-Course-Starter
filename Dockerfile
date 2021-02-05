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

FROM base as test_base
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update \
  && apt-get install --no-install-recommends --no-install-suggests --assume-yes \
  curl \
  bzip2 \
  libgtk-3-0 \
  libdbus-glib-1-2 \
  xvfb \
  && FIREFOX_DOWNLOAD_URL='https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64' \
  && curl -sL "$FIREFOX_DOWNLOAD_URL" | tar -xj -C /opt \
  && ln -s /opt/firefox/firefox /usr/local/bin/ \
  && BASE_URL='https://github.com/mozilla/geckodriver/releases/download' \
  && VERSION=$(curl -sL 'https://api.github.com/repos/mozilla/geckodriver/releases/latest' | grep tag_name | cut -d '"' -f 4) \
  && curl -sL "${BASE_URL}/${VERSION}/geckodriver-${VERSION}-linux64.tar.gz" | tar -xz -C /usr/local/bin \
  && apt-get purge -y \
  curl \
  bzip2 

COPY poetry.lock pyproject.toml /app/
RUN poetry install

FROM test_base as test_watch
COPY ./scripts /app/scripts
RUN chmod +x "scripts/run_tests_watch.sh" && pip3 install argh
ENTRYPOINT [ "scripts/run_tests_watch.sh" ]

FROM test_base as ci
COPY . /app
RUN chmod +x "scripts/run_tests.sh"
ENTRYPOINT [ "scripts/run_tests.sh" ]

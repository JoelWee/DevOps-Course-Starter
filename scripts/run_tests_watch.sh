#!/bin/bash
poetry run pytest tests && poetry run pytest tests_e2e
poetry run watchmedo shell-command \
    --patterns="*.py" \
    --recursive \
    --command='poetry run pytest tests && poetry run pytest tests_e2e' \
    --wait \
    .
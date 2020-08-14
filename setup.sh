#!/bin/bash
poetry install

# Create a .env file from the .env.template
cp -n .env.template .env

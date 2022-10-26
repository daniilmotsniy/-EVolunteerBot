#!/bin/bash
# The main entrypoint to run all the modules

docker-compose down
docker-compose build
docker-compose up -d

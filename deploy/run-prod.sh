#!/bin/bash
set -e
set -x
export DEBUG=0
nohup python3.7 -m pipenv run python3 main.py &
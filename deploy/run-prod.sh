#!/bin/bash
set -e
set -x
export DEBUG=0
python3 -m pipenv shell "python3 main.py"
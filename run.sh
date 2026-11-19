#!/bin/fish

export PYTHONPATH="$PWD/src"

source .venv/bin/activate.fish

code .

python main.py

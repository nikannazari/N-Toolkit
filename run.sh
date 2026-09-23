#!/bin/bash

echo "activating virtual enviriment"
source .venv/bin/activate
echo "activated"

echo "Add python path to virtual env"
export PYTHONPATH="$PWD/src"
echo "exported!"
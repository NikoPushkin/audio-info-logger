#!/bin/bash
base_python_interpreter=""
read -p "Python interpreter: " base_python_interpreter
`$base_python_interpreter -m venv env`
source env/bin/activate
pip install -U pip
pip install -r requirements.txt

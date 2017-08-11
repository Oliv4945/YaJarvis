#!/bin/bash


VENV_NAME='venv'
python3 -m venv "$VENV_NAME"
$VENV_NAME/bin/pip install setuptools --upgrade
$VENV_NAME/bin/pip install -U wheel
$VENV_NAME/bin/pip install -r requirements.txt
$VENV_NAME/bin/python -m spacy download fr

/bin/bash --rcfile "$VENV_NAME/bin/activate"

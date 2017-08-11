#!/bin/bash

# From https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python -m rasa_nlu.train \
	--config "$DIR/config/spacy.json" \
	--data "$DIR/data" \
	--path "$DIR/models"

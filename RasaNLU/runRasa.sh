#!/bin/bash

# From https://stackoverflow.com/questions/59895/getting-the-source-directory-of-a-bash-script-from-within
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python -m rasa_nlu.server -c "$DIR/config/spacy.json" --server_model_dirs="$DIR/models/YaJarvis/"

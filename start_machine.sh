#!/usr/bin/env bash

# get project root directory (location of this script)
ABS_SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE}")")"

# activate python virtualenv
cd "${ABS_SCRIPT_DIR}" || exit
source .venv/bin/activate

# start dmm with src as working directory
cd "${ABS_SCRIPT_DIR}/src" || exit
python3 main.py \
  --config "${ABS_SCRIPT_DIR}/src/datasources/configuration.json" \
  --ingredients "${ABS_SCRIPT_DIR}/src/datasources/ingredients.json" \
  --drinks "${ABS_SCRIPT_DIR}/src/datasources/drinks.json"

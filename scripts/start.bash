#!/bin/bash

# Move out of 'scripts' directory if executed from there
SCRIPT_DIR=$(dirname "$(realpath "$0")")
if [[ $(basename "$SCRIPT_DIR") == "scripts" ]]; then
  cd "$SCRIPT_DIR/.." || exit
  echo "Moved out of 'scripts' directory to $(pwd)"
fi

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate
echo "Virtual environment activated."

# Install requirements
if [ -f "requirements.txt" ]; then
  pip install --upgrade pip
  pip install -r requirements.txt
  echo "Dependencies installed."
fi

jupyter notebook fornagiel_miklas_projekt.ipynb
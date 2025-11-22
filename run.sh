#!/bin/bash

# Activate virtual environment
source ../venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Ollama is not running. Starting it..."
    ollama serve &
    sleep 5
fi

# Run Streamlit app
streamlit run app.py

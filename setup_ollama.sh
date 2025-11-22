#!/bin/bash

echo "Checking for Ollama..."

if ! command -v ollama &> /dev/null; then
    echo "Ollama could not be found."
    echo "Please install Ollama from https://ollama.com/download"
    echo "After installing, run this script again."
    exit 1
fi

echo "Ollama found. Pulling qwen2.5 model..."
ollama pull qwen2.5

echo "Pulling embedding model (optional, handled by python, but good to have)..."
# Note: BGE-M3 is handled by HuggingFaceEmbeddings in python, so we don't need to pull it in Ollama unless we use Ollama for embeddings too.
# We are using HF embeddings for better quality.

echo "Setup complete! Run 'streamlit run app.py' to start."

# Multilingual RAG System Setup

## Prerequisites
1. **Ollama**: You must have [Ollama](https://ollama.com/) installed and running.
   - Mac: Download from website.
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`

## Setup Steps

1. **Install Dependencies** (Already done via agent, but for reference):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Setup Ollama Model**:
   Run the setup script:
   ```bash
   chmod +x setup_ollama.sh
   ./setup_ollama.sh
   ```
   Or manually:
   ```bash
   ollama pull qwen2.5
   ```

3. **Run the App**:
   ```bash
   streamlit run app.py
   ```

## Usage
- Upload PDF or TXT files using the sidebar.
- Wait for processing.
- Chat in Thai or English!

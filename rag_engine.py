import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb

# Configuration
DATA_DIR = "data"
DB_DIR = "chroma_db"
COLLECTION_NAME = "rag_collection"
LLM_MODEL = "qwen2.5"  # or "llama3"
EMBED_MODEL = "BAAI/bge-m3"

def get_llm():
    return Ollama(model=LLM_MODEL, request_timeout=300.0)

def get_embedding_model():
    # BAAI/bge-m3 is excellent for multilingual (including Thai)
    return HuggingFaceEmbedding(model_name=EMBED_MODEL)

def initialize_index():
    # 1. Setup LLM and Embeddings
    Settings.llm = get_llm()
    Settings.embed_model = get_embedding_model()

    # 2. Setup ChromaDB
    db = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 3. Load Data (if exists) or create empty index
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        # Return empty index connected to vector store
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            storage_context=storage_context,
        )
        return index

    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    
    # 4. Create/Update Index
    # Note: In a real app, we'd want to avoid re-indexing everything every time.
    # For this "bare minimum" version, we'll check if the DB is empty or just load.
    # To support "adding files without retraining", we rely on the vector store persistence.
    # If we want to add *new* files, we should use `index.insert(document)`.
    
    # For simplicity in this starter:
    # We will try to load the index from storage first.
    
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        storage_context=storage_context,
    )
    
    # If we want to ensure all files in data/ are indexed, we can do a check.
    # But for now, let's assume the UI handles "add file" -> "index.insert".
    
    return index

def add_file_to_index(file_path, index):
    """Ingests a single file into the existing index."""
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    for doc in documents:
        index.insert(doc)
    return f"Added {file_path} to index."

def get_query_engine(index):
    return index.as_query_engine(streaming=True)

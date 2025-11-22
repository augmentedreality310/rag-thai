import sys
import os

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings("ignore")

try:
    print("Importing rag_engine...")
    from rag_engine import initialize_index, get_query_engine
    
    print("Initializing index (this might download the embedding model)...")
    index = initialize_index()
    print("Index initialized.")
    
    query_engine = get_query_engine(index)
    print("Query engine ready.")
    
    print("Testing query...")
    response = query_engine.query("Hello, are you working?")
    print("Response received:")
    for chunk in response.response_gen:
        print(chunk, end="", flush=True)
    print("\nDone.")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

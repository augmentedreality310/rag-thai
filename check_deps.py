import sys
import pkg_resources

packages = [
    "llama_index.core",
    "llama_index.llms.ollama",
    "llama_index.embeddings.huggingface",
    "llama_index.vector_stores.chroma",
    "streamlit",
    "watchfiles"
]

print("Checking dependencies...")
for package in packages:
    try:
        dist = pkg_resources.get_distribution(package)
        print(f"✅ {package} is installed ({dist.version})")
    except pkg_resources.DistributionNotFound:
        print(f"❌ {package} is NOT installed")
    except Exception as e:
        print(f"⚠️ Error checking {package}: {e}")

print("\nTrying imports...")
try:
    import llama_index.core
    print("✅ import llama_index.core success")
except ImportError as e:
    print(f"❌ import llama_index.core failed: {e}")

try:
    import streamlit
    print("✅ import streamlit success")
except ImportError as e:
    print(f"❌ import streamlit failed: {e}")

import sys

missing = []

try:
    import sentence_transformers
    print("✅ sentence_transformers installed")
except ImportError:
    print("❌ sentence_transformers MISSING")
    missing.append("sentence-transformers")

try:
    import chromadb
    print("✅ chromadb installed")
except ImportError:
    print("❌ chromadb MISSING")
    missing.append("chromadb")

if missing:
    print(f"Need to install: {' '.join(missing)}")
    sys.exit(1)
else:
    sys.exit(0)

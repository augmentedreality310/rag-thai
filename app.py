import streamlit as st
import os
from rag_engine import initialize_index, add_file_to_index, get_query_engine, DATA_DIR

st.set_page_config(page_title="Multilingual RAG (Thai)", layout="wide")

st.title("🇹🇭 Multilingual Local RAG")

# Initialize Session State
if "index" not in st.session_state:
    with st.spinner("Initializing RAG Engine (Loading models... this may take a moment)"):
        try:
            st.session_state.index = initialize_index()
            st.session_state.query_engine = get_query_engine(st.session_state.index)
            st.success("Engine Initialized!")
        except Exception as e:
            st.error(f"Failed to initialize engine: {e}")
            st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar: File Upload
with st.sidebar:
    st.header("Document Management")
    uploaded_files = st.file_uploader("Upload PDF/TXT", accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("Process Files"):
            if not os.path.exists(DATA_DIR):
                os.makedirs(DATA_DIR)
            
            progress_bar = st.progress(0)
            for i, uploaded_file in enumerate(uploaded_files):
                file_path = os.path.join(DATA_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Add to index
                add_file_to_index(file_path, st.session_state.index)
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            st.success(f"Processed {len(uploaded_files)} files!")
            # Refresh query engine just in case
            st.session_state.query_engine = get_query_engine(st.session_state.index)

    if st.button("Reset & Re-index All"):
        with st.spinner("Resetting index..."):
            # Clear Chroma (simple way: delete collection or just re-create)
            # For simplicity, we'll just re-run ingestion on all files in DATA_DIR
            # Ideally we'd drop the collection first.
            try:
                # This is a bit hacky for a simple app, but effective
                import shutil
                if os.path.exists("chroma_db"):
                    shutil.rmtree("chroma_db")
                st.session_state.index = initialize_index()
                
                # Re-ingest all
                if os.path.exists(DATA_DIR):
                    documents = SimpleDirectoryReader(DATA_DIR).load_data()
                    for doc in documents:
                        st.session_state.index.insert(doc)
                
                st.session_state.query_engine = get_query_engine(st.session_state.index)
                st.success("Index reset and all files re-indexed!")
            except Exception as e:
                st.error(f"Error resetting: {e}")

    st.divider()
    st.markdown("### System Info")
    st.info("Running locally with Ollama (qwen2.5) + ChromaDB")

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question (Thai/English)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Stream response
        streaming_response = st.session_state.query_engine.query(prompt)
        
        for chunk in streaming_response.response_gen:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

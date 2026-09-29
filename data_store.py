import os

# Prevent tokenizer parallelism warnings from Hugging Face
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def build_vector_store():
    doc_dir = "documents"
    
    # Ensure the documents directory exists
    if not os.path.exists(doc_dir):
        os.makedirs(doc_dir)
        print(f"Created missing '{doc_dir}' directory.")
            
    documents = []
    
    # Walk through the documents folder and load all supported formats
    if os.path.exists(doc_dir):
        for root, dirs, files in os.walk(doc_dir):
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                try:
                    if ext in ['.txt', '.md']:
                        loader = TextLoader(file_path, encoding='utf-8')
                        documents.extend(loader.load())
                        print(f"Loaded text/markdown file: {file}")
                    elif ext == '.pdf':
                        loader = PyPDFLoader(file_path)
                        documents.extend(loader.load())
                        print(f"Loaded PDF file: {file}")
                except Exception as e:
                    print(f"Error loading file {file}: {e}")

    # Fallback default text if no files are found in the folder
    if not documents:
        from langchain_core.documents import Document
        documents = [
            Document(
                page_content=(
                    "Maison Hygia Support Desk: General wellness products, "
                    "holistic skin barrier repair, circadian support, and customer service."
                )
            )
        ]
        print("No documents found. Using default fallback document.")

    # Split documents into optimal chunks for RAG retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50,
        separators=["\n## ", "\n### ", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(documents)
    
    print("Generating local embeddings using HuggingFace (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Build FAISS vector database from document chunks
    vector_store = FAISS.from_documents(docs, embedding=embeddings)
    vector_store.save_local("faiss_index")
    
    print(f"Success! Indexed {len(docs)} total document chunks into local 'faiss_index'.")

if __name__ == "__main__":
    build_vector_store()
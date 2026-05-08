from  pathlib import Path
import pickle
import faiss
import numpy as np

#Langchain utilities
from langchain_community.document_loaders import PyPDFLoader,CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Sentense transformer for embedding
from sentence_transformers import SentenceTransformer

#Configurations
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR/ 'data'
STORE_DIR = BASE_DIR/'store'
INDEX_PATH = STORE_DIR /'faiss_index' # Path to store FAISS index
CHUNKS_PATH = STORE_DIR /'chunks'  # Path to store document chunks

## ------------------------------------------------------
## Step 1: LOAD DOCUMENTS
## ------------------------------------------------------

#Load all PDFs and CSV from data
def load_docs(data_path: Path):
    docs=[]
    for file in data_path.glob('*.pdf'):
        loader=PyPDFLoader(str(file))
        docs.extend(loader.load())
    for file in data_path.glob('*.csv'):
        loader=CSVLoader(str(file))
        docs.extend(loader.load())
    return docs

## ------------------------------------------------------
## Step 2: SPLIT DOCUMENTS INTO CHUNKS
## ------------------------------------------------------

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)

## ------------------------------------------------------
## Step 3: EMBED the DOCUMENT CHUNKS
## ------------------------------------------------------

def create_embeddings(chunks):
    model=SentenceTransformer(EMBEDDING_MODEL_NAME)
    texts=[chunk.page_content for chunk in chunks]

    #generate embeddings
    embeddings=model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype('float32')
    return embeddings,chunks

## ------------------------------------------------------
## Step 4: STORE the EMBEDDINGS in FAISS
## ------------------------------------------------------

def store_faiss(embeddings,chunks):
    STORE_DIR.mkdir(exist_ok=True)
    dim=embeddings.shape[1]
    index=faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index,str(INDEX_PATH))

    #Save the document chunks to disk
    with open(CHUNKS_PATH,'wb') as f:
        pickle.dump(chunks,f)

## ------------------------------------------------------
## Step 5: Main execution
## ---------------------------------------------------

if __name__=="__main__":
    docs=load_docs(DATA_DIR)
    print(f"Loaded {len(docs)} documents.")

    chunks=split_docs(docs)
    print(f"Split {len(docs)} documents into {len(chunks)} chunks.")
    embeddings,chunks= create_embeddings(chunks)
    print(f"Created embeddings for {len(chunks)} chunks.")

    store_faiss(embeddings,chunks)
    print(f"Processed {len(docs)}  documents into {len(chunks)} chunks and stored in FAISS index")

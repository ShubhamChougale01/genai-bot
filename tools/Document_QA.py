import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

PDF_PATH = "/Users/shubham/genai_bot/Doc/genai_intro.pdf"
INDEX_DIR = "/Users/shubham/genai_bot/Doc/faiss_index"

llm = ChatGroq(
    model="gemma2-9b-it", 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1,
    max_tokens=100,
    top_p=0.9,         
    )

def vector_storage(pdf_path: str, index_dir: str):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(index_dir):
        print("Loading existing FAISS index...")
        return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    else:
        print("No index found. Building FAISS index...")
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(documents)

        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(index_dir)
        print("FAISS index saved.")
        return vectorstore

def rag_chain():
    vectorstore = vector_storage(PDF_PATH, INDEX_DIR)
    retriever = vectorstore.as_retriever(
        search_type="similarity",   
        search_kwargs={
            "k": 5,               
            "fetch_k": 10,
        }
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

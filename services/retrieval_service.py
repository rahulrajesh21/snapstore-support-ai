from langchain_pinecone import PineconeVectorStore
from agent.graph import embedding_model
from services.document_processor import processor
from model.query_chat import QueryChat
from langchain_community.retrievers import BM25Retriever
import os

vector_store = PineconeVectorStore(
    index_name=os.getenv("INDEX_NAME", "shop-support"),
    embedding=embedding_model,
    namespace='policies'
)


def load_keyword():
    """Builds an in-memory BM25 index over all structured markdown chunks."""
    documents = processor("knowledge")
    bm25_retriever = BM25Retriever.from_documents(documents=documents)
    return bm25_retriever


def load_embedding(file_path: str = "knowledge"):
    """Indexes document chunks into Pinecone using structure-aware chunking."""
    chunks = processor(file_path)
    vector_store.add_documents(chunks)
    print(f"Successfully stored {len(chunks)} structure-aware chunks in Pinecone.")


async def user_query(query: QueryChat):
    """Performs dense vector similarity search in Pinecone."""
    documents = await vector_store.asimilarity_search(query=query.query, k=5)
    return documents

from langchain_pinecone import PineconeVectorStore
from agent.graph import embedding_model
from services.document_processor import processor
from model.query_chat import QueryChat
import os

vector_store = PineconeVectorStore(
    index_name=os.getenv("INDEX_NAME","shop-support"),
    embedding= embedding_model,
    namespace='policies'
)


def load_embedding(file_path: str = 'knowledge/Policy.pdf'):
    chunks = processor(file_path)
    vector_store.add_documents(chunks)
    print(f"Successfully stored {len(chunks)} chunks in Pinecone.")


async def user_query(query:QueryChat):
    documents = await vector_store.asimilarity_search(query=query.query,k=5)
    return documents


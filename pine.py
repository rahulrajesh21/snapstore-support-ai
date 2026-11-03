import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Replace 1536 with your embedding_model's dimensions (e.g., 768 for Gemini, 1536 for OpenAI)
pc.create_index(
    name=os.getenv("INDEX_NAME", "shop-support"),
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

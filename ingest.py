from dotenv import load_dotenv
load_dotenv()

from services.retrieval_service import load_embedding

if __name__ == "__main__":
    print("🚀 Starting document ingestion into Pinecone...")
    load_embedding()
    print("✅ Ingestion complete!")
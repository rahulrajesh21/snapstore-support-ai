import sys
from dotenv import load_dotenv

load_dotenv()

from services.retrieval_service import load_embedding

if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "knowledge"
    print(f"Starting structure-aware document ingestion for: {pdf_path}")
    load_embedding(pdf_path)
    print("Ingestion complete.")

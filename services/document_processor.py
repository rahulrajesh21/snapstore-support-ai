from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


def processor():
    loader = PyPDFLoader(
    'knowledge/Policy.pdf'
    )
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
    )

    chunks = splitter.split_documents(pages)

    return chunks


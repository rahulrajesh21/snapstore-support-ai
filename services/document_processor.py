import re
from pathlib import Path
from typing import List, Union
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import pymupdf4llm


def clean_metadata_value(val: str) -> str:
    """Removes markdown formatting characters (*, _, #) from header metadata."""
    if not val:
        return ""
    return re.sub(r'[*_#]', '', str(val)).strip()


def extract_markdown_from_pdf(pdf_path: Path) -> str:
    """
    Extracts structured markdown from a PDF using pymupdf4llm.
    Falls back to standard PyPDFLoader text concatenation if needed.
    """
    try:
        md_text = pymupdf4llm.to_markdown(str(pdf_path))
        if md_text and md_text.strip():
            return md_text
    except Exception as e:
        print(f"Warning: pymupdf4llm failed for {pdf_path.name} ({e}). Falling back to PyPDFLoader.")

    # Fallback to PyPDFLoader
    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load()
    return "\n\n".join(page.page_content for page in pages)


def structure_aware_split(
    md_text: str,
    source_path: Path,
    chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> List[Document]:
    """
    Splits markdown text based on structural headers (#, ##, ###) using
    MarkdownHeaderTextSplitter, and subdivides oversized sections with
    RecursiveCharacterTextSplitter while preserving header hierarchy metadata.
    """
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    # Stage 1: Structure-Aware Header Splitting
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )
    sections = markdown_splitter.split_text(md_text)

    # Attach document metadata and clean header tags
    for sec in sections:
        sec.metadata["source"] = str(source_path)
        sec.metadata["filename"] = source_path.name

        cleaned_h1 = clean_metadata_value(sec.metadata.get("Header 1", ""))
        cleaned_h2 = clean_metadata_value(sec.metadata.get("Header 2", ""))
        cleaned_h3 = clean_metadata_value(sec.metadata.get("Header 3", ""))

        if cleaned_h1:
            sec.metadata["Header 1"] = cleaned_h1
        if cleaned_h2:
            sec.metadata["Header 2"] = cleaned_h2
        if cleaned_h3:
            sec.metadata["Header 3"] = cleaned_h3

        # Construct breadcrumb section path for contextual search
        breadcrumb_parts = [p for p in [cleaned_h1, cleaned_h2, cleaned_h3] if p]
        sec.metadata["section"] = " > ".join(breadcrumb_parts) if breadcrumb_parts else source_path.stem

    # Stage 2: Recursive Character Splitter for oversized sections
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    final_chunks = recursive_splitter.split_documents(sections)
    return final_chunks


def processor(
    path: Union[str, Path] = "knowledge",
    chunk_size: int = 1000,
    chunk_overlap: int = 150
) -> List[Document]:
    """
    Structure-Aware Document Processor:
    Loads one or more PDF files, converts them to structured markdown, and chunks
    them based on document headings while preserving structural metadata.

    Args:
        path: Path to a specific PDF file or a directory containing PDF files.
        chunk_size: Maximum characters per sub-chunk if a section is oversized.
        chunk_overlap: Character overlap between consecutive sub-chunks.

    Returns:
        List of LangChain Document objects with hierarchical metadata.
    """
    target_path = Path(path)

    if not target_path.exists():
        raise FileNotFoundError(f"Path does not exist: {target_path}")

    # Determine all target PDF files
    if target_path.is_file() and target_path.suffix.lower() == ".pdf":
        pdf_files = [target_path]
    elif target_path.is_dir():
        pdf_files = sorted(
            [p for p in target_path.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"]
        )
    else:
        raise ValueError(f"Target path must be a PDF file or a directory with PDFs: {target_path}")

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {target_path}")

    all_chunks: List[Document] = []

    for pdf_file in pdf_files:
        md_text = extract_markdown_from_pdf(pdf_file)
        chunks = structure_aware_split(
            md_text=md_text,
            source_path=pdf_file,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        all_chunks.extend(chunks)

    return all_chunks

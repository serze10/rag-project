from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


DOCS_DIR = "docs"
DB_DIR = "db"


def ingest_documents():

    docs_path = Path(DOCS_DIR)

    if not docs_path.exists():
        raise FileNotFoundError(
            f"Kansiota '{DOCS_DIR}' ei löytynyt."
        )

    pdf_files = list(docs_path.glob("*.pdf"))

    if len(pdf_files) == 0:
        raise ValueError(
            f"Kansiosta '{DOCS_DIR}' ei löytynyt yhtään PDF-tiedostoa."
        )

    print(f"Löytyi {len(pdf_files)} PDF-tiedostoa")

    loader = PyPDFDirectoryLoader(DOCS_DIR)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    return len(documents), len(chunks)


if __name__ == "__main__":

    pages, chunks = ingest_documents()

    print(
        f"Valmis. Ladattiin {pages} sivua ja luotiin {chunks} chunkia."
    )
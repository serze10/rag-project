from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

try:
    from .rag import ask_question, reload_database
    from .ingest import ingest_documents
except ImportError:
    from rag import ask_question, reload_database
    from ingest import ingest_documents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/chat")
def chat(data: dict):

    question = data["question"]

    response = ask_question(question)

    return response


@app.get("/documents")
def list_documents():
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    documents = sorted(
        (path.name for path in docs_dir.glob("*.pdf")),
        key=str.lower,
    )
    return {"documents": documents}


@app.post("/documents")
async def upload_documents(files: list[UploadFile] = File(...)):
    docs_dir = Path(__file__).resolve().parent.parent / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    uploaded = []
    rejected = []

    for uploaded_file in files:
        filename = Path(uploaded_file.filename or "").name

        if not filename.lower().endswith(".pdf"):
            rejected.append(uploaded_file.filename or "")
            continue

        content = await uploaded_file.read()
        (docs_dir / filename).write_bytes(content)
        uploaded.append(filename)

    if not uploaded:
        return {
            "uploaded": [],
            "rejected": rejected,
            "detail": "No PDF files were uploaded.",
        }

    pages, chunks = ingest_documents()
    reload_database()

    return {
        "uploaded": uploaded,
        "rejected": rejected,
        "pages": pages,
        "chunks": chunks,
    }
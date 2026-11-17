from pathlib import Path
import shutil

import gradio as gr

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from ollama import chat

from ingest import ingest_documents


DOCS_DIR = "docs"
DB_DIR = "db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_db():
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )


def upload_pdfs(files):

    if not files:
        return "Ei tiedostoja valittuna."

    docs_dir = Path(DOCS_DIR)
    docs_dir.mkdir(exist_ok=True)

    count = 0

    for file in files:

        source = Path(file)

        destination = docs_dir / source.name

        shutil.copy(source, destination)

        count += 1

    pages, chunks = ingest_documents()

    return (
        f"Lisättiin {count} PDF-tiedostoa.\n"
        f"Ladattiin {pages} sivua.\n"
        f"Luotiin {chunks} chunkia."
    )


def ask_question(question):

    if not question:
        return "", ""

    db = get_db()

    results = db.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        doc.page_content
        for doc in results
    )

    prompt = f"""
Vastaa käyttäjän kysymykseen käyttäen
ensisijaisesti annettua materiaalia.

Jos vastausta ei löydy materiaalista,
sano se rehellisesti.

Materiaali:

{context}

Kysymys:

{question}
"""

    response = chat(
        model="qwen3",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    answer = response["message"]["content"]

    source_text = ""

    for i, doc in enumerate(results, start=1):

        page = doc.metadata.get("page", "tuntematon")
        source = doc.metadata.get(
            "source",
            "tuntematon tiedosto"
        )

        source_text += (
            f"Lähde {i}\n"
            f"Tiedosto: {source}\n"
            f"Sivu: {page}\n\n"
            f"{doc.page_content[:500]}\n\n"
            + "-" * 40
            + "\n\n"
        )

    return answer, source_text


with gr.Blocks() as demo:

    gr.Markdown(
        """
# 📚 PDF RAG Assistant

Lataa PDF:t ja kysy niistä luonnollisella kielellä.
"""
    )

    pdfs = gr.File(
        file_types=[".pdf"],
        file_count="multiple",
        label="PDF-tiedostot"
    )

    upload_btn = gr.Button(
        "Lataa ja indeksoi PDF:t"
    )

    upload_status = gr.Textbox(
        label="Tila"
    )

    upload_btn.click(
        fn=upload_pdfs,
        inputs=pdfs,
        outputs=upload_status
    )

    gr.Markdown("---")

    question = gr.Textbox(
        label="Kysymys"
    )

    ask_button = gr.Button("Kysy")

    answer = gr.Textbox(
        label="Vastaus",
        lines=10
    )

    sources = gr.Textbox(
        label="Lähteet",
        lines=15
    )

    ask_button.click(
        fn=ask_question,
        inputs=question,
        outputs=[answer, sources]
    )

demo.launch()
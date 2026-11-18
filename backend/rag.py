from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path

from ollama import chat


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def load_database():
    return Chroma(
        persist_directory=str(
            Path(__file__).resolve().parent.parent / "db"
        ),
        embedding_function=embeddings,
    )


db = load_database()


def reload_database():
    global db
    db = load_database()


def ask_question(question):

    results = db.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        doc.page_content
        for doc in results
    )

    prompt = f"""
Context:

{context}

Question:

{question}
"""

    response = chat(
        model="qwen3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"]
    }
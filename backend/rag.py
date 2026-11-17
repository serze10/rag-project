from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from ollama import chat


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)


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
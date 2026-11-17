from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from ollama import chat


print("Ladataan embedding-malli...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Ladataan tietokanta...")

db = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)

print("Valmis.")

while True:

    question = input("\nKysymys ('exit' lopettaa): ")

    if question.lower() == "exit":
        break

    results = db.similarity_search(
        question,
        k=3
    )

    print("\nLöydetyt dokumenttipalat:\n")

    for i, doc in enumerate(results, start=1):
        print("=" * 60)
        print(f"Hakutulos {i}")
        print("=" * 60)
        print(doc.page_content[:1000])

    context = "\n\n".join(
        doc.page_content
        for doc in results
    )

    prompt = f"""
Vastaa käyttäjän kysymykseen käyttäen alla olevaa materiaalia.

Jos materiaali ei sisällä vastausta,
sano rehellisesti ettet löydä vastausta.

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
                "content": prompt
            }
        ]
    )

    print("\nVastaus:\n")
    print(response["message"]["content"])
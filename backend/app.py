from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rag import ask_question

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
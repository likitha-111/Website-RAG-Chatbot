from fastapi import FastAPI
from pydantic import BaseModel

from rag.chatbot import ask_chatbot
from rag.vector_store import build_vector_store

app = FastAPI(
    title="Website RAG Chatbot"
)


class QueryRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"message": "Website RAG Chatbot Running"}


@app.post("/build")
def build_db():

    build_vector_store()

    return {
        "status": "Vector DB updated"
    }


@app.post("/chat")
def chat(request: QueryRequest):

    response = ask_chatbot(request.query)

    return response
import os

from dotenv import load_dotenv

from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain
from langchain_groq import ChatGroq
from db.mongo_memory import append_message, get_conversation

from rag.retriever import retrieve_documents


load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0
)

def build_history(messages):

    history = ""

    for msg in messages:

        history += f"""
{msg['role']}: {msg['content']}
"""

    return history


def ask_chatbot(query: str, session_id: str):

    docs = retrieve_documents(query)

    context = "\n\n".join(
        [
            f"Source: {d['title']}\n{d['content']}"
            for d in docs
        ]
    )

    messages = get_conversation(session_id)

    history = build_history(messages)


    prompt = f"""
    <system>
    You are a helpful TechCrunch AI assistant. Your job is to answer user_question using ONLY the provided context and conversation_history.
    <Instructions>
        - Give direct answers without mentioning the existence of context, articles, or conversation history.
        - Use conversation_history only to resolve references and follow-up questions.
        - Combine information from multiple context chunks when necessary.
        - If the answer exists in the context or conversation_history, provide the best possible answer even if the information is spread across multiple chunks or previous turns.
        - You may summarize or rephrase the context naturally.
        - Do NOT make up information outside the context and conversation_history.
        - If the answer truly cannot be found in either the context or the conversation_history, reply exactly: "I don't have information about that in the current articles."
    </Instructions>

    <conversation_history>
        {history}
    </conversation_history>

    <context>
        {context}
    </context>
    </system>

    <user_question>
    {query}
    </user_question>
"""

    response = llm.invoke(prompt)

    answer = response.content

    append_message(
        session_id=session_id,
        role="user",
        content=query
    )

    append_message(
        session_id=session_id,
        role="assistant",
        content=answer,
        sources=[
            {
                "title": d["title"],
                "url": d["source"]
            }
            for d in docs
        ]
    )
    return {
        "answer": answer,
        "sources": [
            {
                "title": d["title"],
                "url": d["source"]
            }
            for d in docs
        ]
    }
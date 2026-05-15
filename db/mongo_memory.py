import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client[os.getenv("MONGO_DB")]

collection = db[os.getenv("MONGO_COLLECTION")]


def create_chat_session(session_id):

    existing = collection.find_one({
        "session_id": session_id
    })

    if not existing:

        collection.insert_one({
            "session_id": session_id,
            "messages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })


def append_message(
    session_id,
    role,
    content,
    sources=None
):

    create_chat_session(session_id)

    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    }

    if sources:

        unique_sources = []
        seen_urls = set()

        for source in sources:

            url = source.get("url")

            if url not in seen_urls:

                unique_sources.append(source)

                seen_urls.add(url)

        message["sources"] = unique_sources

    collection.update_one(
        {"session_id": session_id},
        {
            "$push": {
                "messages": message
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )


def get_conversation(session_id):

    session = collection.find_one({
        "session_id": session_id
    })

    if not session:
        return []

    return session["messages"]
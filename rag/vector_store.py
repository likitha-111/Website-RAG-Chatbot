import json
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from chromadb import PersistentClient

from rag.embeddings import embedding_model
from scraper.rss_scraper import fetch_rss_articles
from scraper.article_parser import extract_article_content


CHROMA_DIR = "chroma_db"

client = PersistentClient(path=CHROMA_DIR)

collection = client.get_or_create_collection(
    name="techcrunch_articles"
)

PROCESSED_FILE = Path("data/processed_urls.json")

if not PROCESSED_FILE.exists():
    PROCESSED_FILE.write_text("[]")


def load_processed_urls():
    return json.loads(PROCESSED_FILE.read_text())


def save_processed_urls(urls):
    PROCESSED_FILE.write_text(json.dumps(urls, indent=2))


def build_vector_store(limit=20):

    articles = fetch_rss_articles(limit)

    processed = load_processed_urls()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )

    new_processed = processed.copy()

    total_chunks = 0

    for article in articles:

        url = article["link"]

        if url in processed:
            continue

        content = extract_article_content(url)

        if not content:
            continue

        chunks = splitter.split_text(content)

        embeddings = embedding_model.encode(chunks).tolist()

        ids = [
            f"{url}_{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            {
                "source": url,
                "title": article["title"]
            }
            for _ in chunks
        ]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

        total_chunks += len(chunks)

        new_processed.append(url)

        print(f"Indexed: {article['title']}")

    save_processed_urls(new_processed)

    print(f"\nTotal chunks stored: {total_chunks}")


if __name__ == "__main__":
    build_vector_store()
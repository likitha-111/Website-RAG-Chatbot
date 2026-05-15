import json
import feedparser
from pathlib import Path

RSS_URL = "https://techcrunch.com/feed/"

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

RAW_ARTICLES = DATA_DIR / "raw_articles.json"


def fetch_rss_articles(limit: int = 20):
    feed = feedparser.parse(RSS_URL)

    articles = []

    for entry in feed.entries[:limit]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "")
        })

    with open(RAW_ARTICLES, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    return articles


if __name__ == "__main__":
    data = fetch_rss_articles()
    print(f"Fetched {len(data)} articles")
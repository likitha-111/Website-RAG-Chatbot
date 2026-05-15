import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def extract_article_content(url: str):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)

        soup = BeautifulSoup(response.text, "html.parser")

        article = soup.find("div", class_="entry-content")

        if not article:
            return None

        paragraphs = article.find_all("p")

        content = "\n".join(
            p.get_text(strip=True)
            for p in paragraphs
        )

        return content

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
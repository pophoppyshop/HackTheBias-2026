import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

API_KEY = os.getenv("MY_API_KEY")
CX = os.getenv("GOOGLE_CX")

def google_search(query, num_results=5):
    
    #Perform a Google Custom Search and return raw JSON data.
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": CX,
        "num": num_results
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()

def extract_articles(search_data, max_results=10):
    
    #Extract article titles, websites, and URLs from search results.
    
    articles = []

    for item in search_data.get("items", []):
        title = item.get("title")
        link = item.get("link")

        if not title or not link:
            continue

        domain = urlparse(link).netloc.lower().replace("www.", "")

        articles.append({
            "title": title,
            "website": domain,
            "url": link
        })

        if len(articles) >= max_results:
            break

    return articles


def fetch_first_paragraphs(url, n=2, timeout=10, min_len=30):
    """
    Fetch the page at `url`, extract paragraph texts, filter out
    very short paragraphs, and return the first `n` paragraphs.
    Returns an empty list on failure.
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; fetch-bot/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        # checks if the HTTP connection was successful
    except Exception:
        return []

    # Use the built-in parser to avoid requiring the lxml dependency
    soup = BeautifulSoup(r.text, "html.parser")
    paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
    # Filter out very short paragraphs (e.g., nav, disclaimers)
    paragraphs = [p for p in paragraphs if len(p) >= min_len]
    return paragraphs[:n]

def run_query(query):
    data = google_search(query)

    total_results = int(
        data.get("searchInformation", {}).get("totalResults", 0)
    )

    print(f"\nQuery: {query}")
    print(f"Total results reported: {total_results}")

    if total_results == 0:
        print("No results found.")
        return []

    articles = extract_articles(data)

    print("\nTop articles (first 2 paragraphs):")
    for i, article in enumerate(articles, start=1):
        print(f"{i}. {article['title']} ({article['website']})")
        first_two = fetch_first_paragraphs(article["url"], n=2)
        if first_two:
            for p in first_two:
                print("  ", p)
        else:
            print("  [could not fetch or extract preview]")
        # polite pause to avoid hammering servers
        time.sleep(0.5)

    return articles

if __name__ == "__main__":
    run_query("Artificial Intelligence in Healthcare")

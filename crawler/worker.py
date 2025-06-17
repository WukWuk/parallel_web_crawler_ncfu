import requests
from bs4 import BeautifulSoup


def crawl_page(url, depth):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception:
        return set()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()

    for tag in soup.find_all('a', href=True):
        href = tag['href']
        if href.startswith('http'):
            links.add(href)
    print(f"Processed page {url} (found links: {len(links)})")
    return links

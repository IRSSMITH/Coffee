import requests
from bs4 import BeautifulSoup
import sqlite3
import re

# Database setup
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS pages (url TEXT UNIQUE, title TEXT, content TEXT)")
conn.commit()

# Crawler function
def crawl(url, depth=2):
    if depth == 0:
        return
    
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "No Title"
        content = re.sub(r'\s+', ' ', soup.get_text()).strip()
        
        cursor.execute("INSERT OR IGNORE INTO pages (url, title, content) VALUES (?, ?, ?)", (url, title, content))
        conn.commit()

        links = [a.get('href') for a in soup.find_all('a', href=True)]
        for link in links:
            if link.startswith("http"):  # Only follow absolute links
                crawl(link, depth-1)

    except Exception as e:
        print(f"Failed to crawl {url}: {e}")

# Start crawling from seed URLs
seed_urls = ["https://en.wikipedia.org/wiki/Main_Page", "https://news.ycombinator.com/"]
for url in seed_urls:
    crawl(url, depth=2)

conn.close()

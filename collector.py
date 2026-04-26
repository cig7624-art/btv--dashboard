import feedparser
import pandas as pd
from datetime import datetime
from urllib.parse import quote

keywords = ["B tv+", "비플", "B tv 플러스", "B tv plus", "B tv+ max"]

rows = []

for keyword in keywords:
    query = quote(keyword)
    url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)

    for entry in feed.entries[:10]:
        rows.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "keyword": keyword,
            "platform": "Google News",
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "mention": 1,
            "sentiment": "neutral"
        })

columns = ["date", "keyword", "platform", "title", "link", "mention", "sentiment"]
df = pd.DataFrame(rows, columns=columns)

try:
    old = pd.read_csv("data.csv")
    df = pd.concat([old, df], ignore_index=True)
except Exception:
    pass

df = df.drop_duplicates(subset=["title", "link"], keep="last")
df.to_csv("data.csv", index=False, encoding="utf-8-sig")

print(f"Updated data.csv with {len(rows)} new rows")

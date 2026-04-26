import feedparser
import pandas as pd
from datetime import datetime

keywords = ["B tv+", "비플", "B tv 플러스", "B tv+ max", "B tv plus"]

rows = []

for keyword in keywords:
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)

    for entry in feed.entries[:10]:
        title = entry.title
        link = entry.link

        rows.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "keyword": keyword,
            "platform": "Google News",
            "title": title,
            "link": link,
            "mention": 1,
            "sentiment": "neutral"
        })

df = pd.DataFrame(rows)

try:
    old = pd.read_csv("data.csv")
    df = pd.concat([old, df], ignore_index=True)
except:
    pass

df = df.drop_duplicates(subset=["title", "link"])
df.to_csv("data.csv", index=False, encoding="utf-8-sig")

import feedparser
import pandas as pd
from datetime import datetime
from urllib.parse import quote

sources = [
    ("B tv+", "B tv+"),
    ("비플", "B tv+"),
    ("B tv+ max", "B tv+"),
    ("넷플릭스 인기작", "OTT_TOP"),
    ("티빙 인기작", "OTT_TOP"),
    ("디즈니플러스 인기작", "OTT_TOP"),
    ("쿠팡플레이 인기작", "OTT_TOP"),
    ("OTT 화제작", "OTT_TOP"),
    ("넷플릭스 신작", "NEW_RELEASE"),
    ("티빙 신작", "NEW_RELEASE"),
    ("디즈니플러스 신작", "NEW_RELEASE"),
    ("쿠팡플레이 신작", "NEW_RELEASE"),
    ("이번주 OTT 신작", "NEW_RELEASE"),
    ("한국 드라마 화제작", "GENRE_SIGNAL"),
    ("범죄 스릴러 드라마", "GENRE_SIGNAL"),
    ("가족 영화 추천", "GENRE_SIGNAL"),
    ("키즈 애니메이션 신작", "GENRE_SIGNAL"),
]

rows = []

for keyword, category in sources:
    query = quote(keyword)
    url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)

    for entry in feed.entries[:10]:
        rows.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "keyword": keyword,
            "category": category,
            "platform": "Google News",
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "mention": 1,
            "sentiment": "neutral"
        })

columns = ["date", "keyword", "category", "platform", "title", "link", "mention", "sentiment"]
df = pd.DataFrame(rows, columns=columns)

try:
    old = pd.read_csv("data.csv")
    if "category" not in old.columns:
        old["category"] = "ETC"
    df = pd.concat([old, df], ignore_index=True)
except Exception:
    pass

df = df.drop_duplicates(subset=["title", "link"], keep="last")
df.to_csv("data.csv", index=False, encoding="utf-8-sig")

print(f"Updated data.csv with {len(rows)} new rows")

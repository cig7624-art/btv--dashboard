import streamlit as st
import pandas as pd

st.title("📊 B tv+ 시장 반응 대시보드")

df = pd.read_csv("data.csv")

st.subheader("🧠 오늘 한줄 인사이트")

total = df["mention"].sum()
top_keyword = df.sort_values("mention", ascending=False).iloc[0]["keyword"]

st.subheader("📰 오늘 주요 뉴스")

latest_news = df.sort_values("date", ascending=False).head(10)

for i, row in latest_news.iterrows():
    st.markdown(f"- [{row['title']}]({row['link']})")

st.subheader("📺 B tv+ 관련 뉴스")

btv = df[df["keyword"].str.contains("B tv|비플", case=False)]

for i, row in btv.head(10).iterrows():
    st.markdown(f"- [{row['title']}]({row['link']})")

st.write(f"오늘 총 언급량 {total}건, '{top_keyword}' 중심으로 화제 형성")

st.subheader("🔥 오늘 언급량")
st.write(df.groupby("keyword")["mention"].sum())

st.subheader("📈 플랫폼별 언급량")
st.bar_chart(df.groupby("platform")["mention"].sum())

st.subheader("💬 감성 비율")
st.write(df["sentiment"].value_counts())

st.subheader("🎬 OTT 화제 콘텐츠 TOP")

top_contents = df.sort_values("mention", ascending=False).head(5)

for i, row in top_contents.iterrows():
    st.write(f"{row['keyword']} - {row['mention']}건")

st.subheader("⚡ 오늘 핫 키워드")

hot = df.sort_values("mention", ascending=False).head(3)
st.write(hot["keyword"].tolist())

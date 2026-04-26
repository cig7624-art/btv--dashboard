import streamlit as st
import pandas as pd

st.set_page_config(page_title="B tv+ 콘텐츠 시장 대시보드", layout="wide")

st.title("📊 B tv+ 콘텐츠 시장 대시보드")

df = pd.read_csv("data.csv")

if "category" not in df.columns:
    df["category"] = "ETC"

df["mention"] = pd.to_numeric(df["mention"], errors="coerce").fillna(1)

today_total = int(df["mention"].sum())
top_keyword = df.groupby("keyword")["mention"].sum().sort_values(ascending=False).index[0]

btv_count = int(df[df["category"] == "B tv+"]["mention"].sum())
ott_count = int(df[df["category"] == "OTT_TOP"]["mention"].sum())

st.subheader("🧠 오늘의 한 줄 인사이트")
st.info(f"오늘 수집된 콘텐츠 시장 신호는 총 {today_total}건이며, 현재는 '{top_keyword}' 관련 언급이 가장 두드러집니다.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("B tv+ 관련 신호", f"{btv_count}건")

with col2:
    st.metric("OTT 화제 콘텐츠 신호", f"{ott_count}건")

with col3:
    st.metric("오늘 핵심 키워드", top_keyword)

st.divider()

st.subheader("📰 오늘의 주요뉴스 TOP 3")
latest_news = df.sort_values("date", ascending=False).head(3)

for i, row in latest_news.iterrows():
    st.markdown(f"""
    <div style="padding:14px; border:1px solid #ddd; border-radius:12px; margin-bottom:10px;">
        <b>{row['title']}</b><br>
        <span style="color:gray;">{row['keyword']} · {row['platform']}</span><br>
        <a href="{row['link']}" target="_blank">기사 보기</a>
    </div>
    """, unsafe_allow_html=True)

st.subheader("📺 B tv+ 관련뉴스 TOP 3")
btv_news = df[df["category"] == "B tv+"].sort_values("date", ascending=False).head(3)

for i, row in btv_news.iterrows():
    st.markdown(f"""
    <div style="padding:14px; border:1px solid #ddd; border-radius:12px; margin-bottom:10px;">
        <b>{row['title']}</b><br>
        <span style="color:gray;">{row['keyword']} · {row['platform']}</span><br>
        <a href="{row['link']}" target="_blank">기사 보기</a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.subheader("🎬 오늘 OTT 화제 콘텐츠 TOP 10")
ott = df[df["category"] == "OTT_TOP"]

if len(ott) > 0:
    ott_top = ott.groupby("keyword")["mention"].sum().sort_values(ascending=False).head(10)
    st.bar_chart(ott_top)
else:
    st.write("아직 OTT 화제 콘텐츠 데이터가 없습니다.")

st.subheader("🆕 이번주 신작 레이더")
new_release = df[df["category"] == "NEW_RELEASE"].sort_values("date", ascending=False).head(8)

for i, row in new_release.iterrows():
    st.markdown(f"- [{row['title']}]({row['link']})")

st.subheader("💡 B tv+ 편성 기회 신호")
genre = df[df["category"] == "GENRE_SIGNAL"]

if len(genre) > 0:
    top_genre = genre.groupby("keyword")["mention"].sum().sort_values(ascending=False).head(5)
    for keyword, count in top_genre.items():
        st.write(f"• **{keyword}** 관련 신호 {int(count)}건 → 특집관/큐레이션 후보")
else:
    st.write("아직 편성 기회 신호가 없습니다.")

st.divider()

st.subheader("⚡ 급등 키워드")
hot = df.groupby("keyword")["mention"].sum().sort_values(ascending=False).head(5)
st.write(list(hot.index))

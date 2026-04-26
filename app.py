import streamlit as st
import pandas as pd

st.title("📊 B tv+ 시장 반응 대시보드")

df = pd.read_csv("data.csv")

st.subheader("🔥 오늘 언급량")
st.write(df.groupby("keyword")["mention"].sum())

st.subheader("📈 플랫폼별 언급량")
st.bar_chart(df.groupby("platform")["mention"].sum())

st.subheader("💬 감성 비율")
st.write(df["sentiment"].value_counts())

st.subheader("🎬 인기 콘텐츠")
st.write(df.sort_values("mention", ascending=False)[["keyword","mention"]].head(5))
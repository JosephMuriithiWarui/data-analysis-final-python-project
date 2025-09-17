
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("metadata/metadata.csv")
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["year"] = df["publish_time"].dt.year
    df = df.dropna(subset=["title", "publish_time"])
    return df

df = load_data()

st.title("📊 CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers interactively.")

# Sidebar: Year range filter
year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.slider("Select Year Range", year_min, year_max, (2020, 2021))
filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# Publications by Year
st.subheader("Publications by Year")
year_counts = filtered["year"].value_counts().sort_index()
st.bar_chart(year_counts)

# Top 10 Journals
st.subheader("Top 10 Journals")
top_journals = filtered["journal"].value_counts().head(10)
st.bar_chart(top_journals)

# Word Cloud of Titles
st.subheader("Word Cloud of Titles")
titles_text = " ".join(filtered["title"].dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles_text)

plt.figure(figsize=(10,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(plt)

# Sample Data Table
st.subheader("Sample Data")
st.dataframe(filtered.head(20))

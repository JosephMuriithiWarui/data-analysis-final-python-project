# cord19_analysis.py
# Step 1: Load and Explore
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from collections import Counter

# Load dataset
df = pd.read_csv("metadata/metadata.csv")

# Basic exploration
print("First 5 rows:")
print(df.head())
print("\nShape:", df.shape)
print("\nData types and info:")
print(df.info())
print("\nMissing values in important columns:")
print(df[["title", "abstract", "publish_time", "journal"]].isnull().sum())
print("\nDescriptive stats:")
print(df.describe())

# Step 2: Clean and Prepare
df_clean = df.dropna(subset=["title", "publish_time"]).copy()
df_clean["publish_time"] = pd.to_datetime(df_clean["publish_time"], errors="coerce")
df_clean["year"] = df_clean["publish_time"].dt.year
df_clean["abstract_word_count"] = df_clean["abstract"].fillna("").apply(lambda x: len(x.split()))

print("\nCleaned dataset preview:")
print(df_clean.head())

# Step 3: Analysis & Visualization

# 3.1 Publications by Year
year_counts = df_clean["year"].value_counts().sort_index()
plt.figure(figsize=(8,5))
plt.bar(year_counts.index, year_counts.values)
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.show()

# 3.2 Top 10 Journals
top_journals = df_clean["journal"].value_counts().head(10)
plt.figure(figsize=(8,5))
top_journals.plot(kind="bar")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.ylabel("Paper Count")
plt.show()

# 3.3 Most Frequent Words in Titles
titles_text = " ".join(df_clean["title"].dropna()).lower()
words = re.findall(r"\b[a-z]{4,}\b", titles_text)
word_counts = Counter(words).most_common(20)
print("\nTop 20 most frequent words in titles:")
print(word_counts)

# 3.4 Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(titles_text)
plt.figure(figsize=(10,6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
plt.show()

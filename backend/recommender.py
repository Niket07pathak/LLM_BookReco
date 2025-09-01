import os
from typing import List, Dict

import pandas as pd
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import Qdrant


# ---- Embeddings (uses local HF cache after first download) ----
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
emb = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True, "batch_size": 64},
)

# ---- Qdrant client & vectorstore ----
load_dotenv()
Qdrant_URL = os.getenv("Qdrant_URL")
Qdrant_API_KEY = os.getenv("Qdrant_API_KEY")
Qdrant_name = os.getenv("Qdrant_name")

qdrant_client = QdrantClient(url=Qdrant_URL, api_key=Qdrant_API_KEY)

vectorstore = Qdrant(
    client=qdrant_client,
    collection_name=Qdrant_name,
    embeddings=emb, 
)

def retrive_books(
    query: str,
    category: str = None,
    tone: str = None,
    initial_recommendations: int = 50,
    final_recommendations: int = 10,
) -> List[Dict]:
    # Retrieve docs
    docs = vectorstore.similarity_search(query, k=initial_recommendations)

    if not docs:
        return []

    # Flatten into DataFrame
    rows = [{"content": d.page_content, **(d.metadata or {})} for d in docs]
    books_df = pd.DataFrame(rows)

    # Category filter (you said these columns are guaranteed to exist)
    if category != "All":
        book_recs = books_df[books_df["simple_categories"] == category].head(final_recommendations)
    else:
        book_recs = books_df.head(final_recommendations)

    # Tone sort
    if tone == "Happy":
        book_recs = book_recs.sort_values(by="joy", ascending=False).head(final_recommendations)
    elif tone == "Surprising":
        book_recs = book_recs.sort_values(by="surprise", ascending=False).head(final_recommendations)
    elif tone == "Angry":
        book_recs = book_recs.sort_values(by="anger", ascending=False).head(final_recommendations)
    elif tone == "Suspenseful":
        book_recs = book_recs.sort_values(by="fear", ascending=False).head(final_recommendations)
    elif tone == "Sad":
        book_recs = book_recs.sort_values(by="sadness", ascending=False).head(final_recommendations)

    return book_recs.reset_index(drop=True).to_dict(orient="records")

def recommender(
        query: str,
        category: str,
        tone: str ,
):
    recommendations = retrive_books(
        query=query,
        category=category,
        tone=tone)
    results = []
    for book in recommendations:
        desc = book["content"] 
        desc_split = desc.split()
        desc_truncated = " ".join(desc_split[:25])+"..."

        
        authors_split = book["authors"].split(";")
        if len(authors_split) == 2:
            authors_str = f"{authors_split[0]} and {authors_split[1]}"
        elif len(authors_split) > 2:
            authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
        else:
            authors_str = book["authors"]
    
        thumb = book.get("thumbnail")

        if not thumb or pd.isna(thumb):
            large_thumb = url_for("static", filename="cover-not-found.jpg")
        else:
            if thumb.startswith("http://books.google.com"):
                thumb = "https://" + thumb[len("http://"):]
            large_thumb = thumb + "&fife=w800"

       ## caption = f"{book['title_subtitle']} by {authors_str}: {desc_truncated}"
        caption = f"{book['title_subtitle']} by {authors_str}"
        
        results.append((large_thumb, caption))
    return results
    

if __name__ == "__main__":
    try:
        results = recommender(
            "preacher in Iowa, multi-generational",
            category="All",
            tone="Surprising"
        )
        if not results:
            print("No results.")
        else:
            for i, (thumb, cap) in enumerate(results[:2], 1):
                print(f"{i}. {thumb} | {cap}")
    except Exception:
        import traceback
        traceback.print_exc()

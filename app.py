from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from backend.recommender import recommender   

app = Flask(__name__)
categories = ["All", "Fiction", "Mystery", "Fantasy", "Non-Fiction"]
tones = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]


@app.get("/healthz")
def health():
    return jsonify({"ok": True})

@app.get("/")
def index():
    return render_template("index.html", categories=categories, tones=tones, results=None)



@app.errorhandler(Exception)
def handle_err(e):
    return jsonify({"error": str(e)}), 500


@app.route("/recommend", methods=["GET"])
def recommend_endpoint():
    query = request.args.get("query", "").strip()
    category = request.args.get("category", "All")
    tone = request.args.get("tone", "All")

    results = recommender(query, category, tone)
    return render_template(
    "index.html",
    categories=categories,
    tones=tones,
    results=results,
    prev_query=query,
    prev_category=category,
    prev_tone=tone,
)



@app.post("/api/recommend")
def api_recommend():
    data = request.get_json(force=True) or {}
    query = (data.get("query") or "").strip()
    category = data.get("category", "All")
    tone = data.get("tone", "All")

    results = recommender(query, category, tone)  # list[(thumb, caption)]
    return jsonify({"results": [{"thumbnail": t, "caption": c} for (t, c) in results]})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)

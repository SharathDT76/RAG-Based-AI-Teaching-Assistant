import faiss
from flask import Flask, render_template, request, jsonify
import logging
import os
import time
import numpy as np
import pandas as pd
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import (
    SIMILARITY_THRESHOLD,
    DEBUG,
    RATE_LIMIT
)
from services.retrieval_service import (
    retrieve_chunks
)
from services.embedding_service import create_embedding

from data.video_data import video_links
# ==========================================
# LOGGING
# ==========================================

os.makedirs(
    "logs",
    exist_ok=True
)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)

app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)
# ==========================================
# LOAD EMBEDDINGS
# ==========================================

df = pd.read_parquet(
    "data/embeddings.parquet"
)

index = faiss.read_index(
    "data/faiss.index"
)

logging.info(
    "FAISS Index Loaded"
)
logging.info(
    "Embeddings Loaded"
)

logging.info(
    f"Total Chunks: {len(df)}"
)
logging.info(
    "Application Started"
)
if DEBUG:
    logging.info(
        "Running in DEBUG mode"
    )


# ==========================================
# HOME PAGE
# ==========================================
@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })
@app.errorhandler(429)
def ratelimit_handler(e):

    return jsonify({
        "error":
        "Too many requests. Please try again later."
    }), 429
# ==========================================
# SEARCH API
# ==========================================
@app.route("/ask", methods=["POST"])
@limiter.limit(RATE_LIMIT)
def ask():

    try:
        start_time_request = time.time()

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON received"
            }), 400

        incoming_query = data.get(
            "question",
            ""
        ).strip()

        if not incoming_query:

            return jsonify({
                "error": "Question required"
            }), 400
        if len(incoming_query) > 500:

            return jsonify({
                "error":
                "Question too long"
            }), 400

        logging.info(
            f"Query: {incoming_query}"
        )

        # ==========================================
        # CREATE QUERY EMBEDDING
        # ==========================================
        question_embedding = create_embedding(
            incoming_query
        )

        # ==========================================
        # SIMILARITY SEARCH
        # ==========================================
        new_df, similarities, max_indx = (
            retrieve_chunks(
                question_embedding,
                index,
                df
            )
        )

        # ==========================================
        # BUILD HTML
        # ==========================================
        results_html = ""

        added_videos = set()

        for rank, (_, row) in enumerate(
            new_df.iterrows()
        ):

            similarity_score = similarities[
                rank
            ]

            # Skip weak matches
            if similarity_score < SIMILARITY_THRESHOLD:
                continue

            video_number = int(row["number"])

            # Avoid duplicates
            if video_number in added_videos:
                continue

            added_videos.add(video_number)

            # Skip missing videos
            if video_number not in video_links:
                continue

            youtube_id = video_links[
                video_number
            ]["youtube_id"]

            # Start 5 seconds earlier
            start_time = max(
                0,
                int(row["start"]) - 5
            )

            # YouTube URL
            watch_url = (
                f"https://www.youtube.com/watch?"
                f"v={youtube_id}&t={start_time}s"
            )

            # Thumbnail
            thumbnail = (
                f"https://img.youtube.com/vi/"
                f"{youtube_id}/hqdefault.jpg"
            )

            # ==========================================
            # VIDEO CARD
            # ==========================================
            results_html += f"""

            <div class="yt-card">

                <img
                    src="{thumbnail}"
                    class="yt-thumbnail"
                >

                <div class="yt-info">

                    <div class="yt-title">
                        {row['title']}
                    </div>

                    <div class="yt-meta">
                        Video #{video_number}
                        •
                        {round(similarity_score * 100)}% Match
                    </div>

                    <div class="yt-time">
                        {row['start']}s → {row['end']}s
                    </div>

                    <div class="yt-description">
                        {row['text'][:350]}...
                    </div>

                    <a
                        href="{watch_url}"
                        target="_blank"
                        class="yt-button"
                    >
                        ▶ Watch From Timestamp
                    </a>

                </div>

            </div>
            """

        # ==========================================
        # NO RESULTS
        # ==========================================
        if not results_html:

            results_html = """

            <div class="no-results">

                No relevant videos found.

            </div>
            """

        elapsed = round(
            time.time() - start_time_request,
            2
        )

        logging.info(
            f"Search completed in {elapsed}s"
        )

        return jsonify({
            "answer": results_html
        })

    except Exception:

        logging.exception(
            "Search Failed"
        )

        return jsonify({
            "answer": """
            <div class="error-box">
                Something went wrong.
            </div>
            """
        }), 500

# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":

    app.run(debug=DEBUG)
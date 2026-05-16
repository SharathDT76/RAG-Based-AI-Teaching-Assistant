from flask import Flask, render_template, request, jsonify
import requests
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from video_data import video_links

app = Flask(__name__)

# ==========================================
# LOAD EMBEDDINGS
# ==========================================
df = pd.read_parquet("embeddings.parquet")

embedding_matrix = np.vstack(
    df["embedding"].values
)

print("Embeddings Loaded")
print(f"Total Chunks: {len(df)}")

# ==========================================
# CREATE EMBEDDING
# ==========================================
def create_embedding(text):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text
        }
    )

    r.raise_for_status()

    return r.json()["embeddings"][0]

# ==========================================
# HOME PAGE
# ==========================================
@app.route("/")
def home():

    return render_template("index.html")

# ==========================================
# SEARCH API
# ==========================================
@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        incoming_query = data["question"]

        # ==========================================
        # CREATE QUERY EMBEDDING
        # ==========================================
        question_embedding = create_embedding(
            incoming_query
        )

        # ==========================================
        # SIMILARITY SEARCH
        # ==========================================
        similarities = cosine_similarity(
            embedding_matrix,
            [question_embedding]
        ).flatten()

        top_results = 8

        max_indx = similarities.argsort()[::-1][
            :top_results
        ]

        new_df = df.iloc[max_indx]

        # ==========================================
        # BUILD HTML
        # ==========================================
        results_html = ""

        added_videos = set()

        for rank, (_, row) in enumerate(
            new_df.iterrows()
        ):

            similarity_score = similarities[
                max_indx[rank]
            ]

            # Skip weak matches
            if similarity_score < 0.55:
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

        return jsonify({
            "answer": results_html
        })

    except Exception as e:

        print(e)

        return jsonify({
            "answer": f"""

            <div class="error-box">

                <h2>Error</h2>

                <p>{str(e)}</p>

            </div>
            """
        })

# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":

    app.run(debug=True)
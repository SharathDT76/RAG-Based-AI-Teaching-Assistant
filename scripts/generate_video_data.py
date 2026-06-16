import yt_dlp
import re

PLAYLIST_URL = (
    "https://www.youtube.com/playlist?"
    "list=PLu0W_9lII9agq5TrH9XLIKQvv0iaF2X3w"
)

ydl_opts = {
    "quiet": True,
    "extract_flat": True,
    "skip_download": True
}

video_data = {}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:

    info = ydl.extract_info(
        PLAYLIST_URL,
        download=False
    )

    entries = info["entries"]

    for video in entries:

        title = video["title"]

        youtube_id = video["id"]

        # =====================================
        # EXTRACT VIDEO NUMBER
        # =====================================
        match = re.search(
            r"#(\d+)",
            title
        )

        if match:

            video_number = int(
                match.group(1)
            )

            video_data[video_number] = {

                "title": title,

                "youtube_id": youtube_id,

                "url":
                f"https://youtube.com/watch?v={youtube_id}"
            }

# =====================================
# SAVE FILE
# =====================================
with open(
    "video_data.py",
    "w",
    encoding="utf-8"
) as f:

    f.write("video_links = ")

    f.write(
        repr(video_data)
    )

print(
    f"Generated "
    f"{len(video_data)} videos"
)
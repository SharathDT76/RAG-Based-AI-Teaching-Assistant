from faster_whisper import WhisperModel
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================= CONFIG =================
audio_folder = "audios"
output_folder = "jsons"

os.makedirs(output_folder, exist_ok=True)

MODEL_SIZE = "large-v3"

# RTX 4070 can handle this comfortably
MAX_WORKERS = 2

# Better semantic chunking
CHUNK_SIZE = 300    # characters
OVERLAP_WORDS = 25    # preserve context


# ================= LOAD MODEL =================
model = WhisperModel(
    MODEL_SIZE,
    device="cuda",
    compute_type="float16"
)


# ================= PROCESS FUNCTION =================
def process_audio(audio):

    if "_" not in audio:
        return

    output_path = f"{output_folder}/{audio}.json"

    # Skip already processed files
    if os.path.exists(output_path):
        print(f"Skipping {audio}")
        return

    try:

        number = audio.split("_")[0]

        # Remove .mp3 extension
        title = "_".join(audio.split("_")[1:]).replace(".mp3", "")

        print(f"\nProcessing {audio}")

        segments, info = model.transcribe(
            f"{audio_folder}/{audio}",
            language="hi",
            task="translate",
            beam_size=1
        )

        chunks = []
        full_text = ""

        current_chunk = ""

        chunk_start = None
        chunk_end = None

        # ================= BUILD LARGER CHUNKS =================
        for seg in segments:

            text = seg.text.strip()

            if not text:
                continue

            full_text += text + " "

            # First segment in chunk
            if chunk_start is None:
                chunk_start = seg.start

            chunk_end = seg.end

            current_chunk += " " + text

            # Save chunk when large enough
            if len(current_chunk) >= CHUNK_SIZE:

                chunks.append({
                    "number": int(number),
                    "title": title,
                    "start": round(chunk_start, 2),
                    "end": round(chunk_end, 2),
                    "text": current_chunk.strip()
                })

                # ================= OVERLAP PRESERVATION =================
                words = current_chunk.split()

                current_chunk = " ".join(
                    words[-OVERLAP_WORDS:]
                )

                chunk_start = seg.start

        # ================= SAVE REMAINING CHUNK =================
        if current_chunk.strip():

            chunks.append({
                "number": int(number),
                "title": title,
                "start": round(chunk_start, 2),
                "end": round(chunk_end, 2),
                "text": current_chunk.strip()
            })

        # ================= FINAL OUTPUT =================
        output = {
            "number": int(number),
            "title": title,
            "chunks": chunks,
            "text": full_text.strip()
        }

        # ================= SAVE JSON =================
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                output,
                f,
                ensure_ascii=False,
                indent=2
            )

        print(
            f"Completed {audio} | "
            f"Chunks Created: {len(chunks)}"
        )

    except Exception as e:
        print(f"❌ Error processing {audio}: {e}")


# ================= MAIN =================
audios = os.listdir(audio_folder)

with ThreadPoolExecutor(
    max_workers=MAX_WORKERS
) as executor:

    futures = [
        executor.submit(process_audio, audio)
        for audio in audios
    ]

    for future in as_completed(futures):
        future.result()

print("\n===================================")
print("All Audio Files Processed")
print("===================================")
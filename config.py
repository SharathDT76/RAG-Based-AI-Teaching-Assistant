import os
from dotenv import load_dotenv

load_dotenv()

# =====================================
# Ollama
# =====================================
OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)

# =====================================
# Search Settings
# =====================================
TOP_RESULTS = int(
    os.getenv("TOP_RESULTS", 8)
)

SIMILARITY_THRESHOLD = float(
    os.getenv(
        "SIMILARITY_THRESHOLD",
        0.55
    )
)

# =====================================
# Flask Settings
# =====================================
DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"

# =====================================
# Logging
# =====================================
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)
RATE_LIMIT = "20 per minute"
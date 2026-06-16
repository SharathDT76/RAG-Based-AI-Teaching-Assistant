import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parent.parent
    )
)

from app import app


def test_health():

    client = app.test_client()

    response = client.get(
        "/health"
    )

    assert response.status_code == 200
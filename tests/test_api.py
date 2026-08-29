import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.skipif(
    "DB_USER" not in os.environ,
    reason="integration test: requires database credentials in the environment",
)
def test_messages_reads_from_database():
    response = client.get("/messages")
    assert response.status_code == 200
    bodies = [row["body"] for row in response.json()]
    assert "hello from postgres" in bodies

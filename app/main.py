import os

import psycopg
from fastapi import FastAPI, HTTPException

app = FastAPI(title="demo-app")


def _dsn() -> str:
    # Credentials always arrive through the environment at runtime; they are
    # never read from files in the repository nor baked into the image.
    return (
        f"host={os.environ.get('DB_HOST', 'localhost')} "
        f"port={os.environ.get('DB_PORT', '5432')} "
        f"dbname={os.environ.get('DB_NAME', 'demo')} "
        f"user={os.environ['DB_USER']} "
        f"password={os.environ['DB_PASSWORD']}"
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/messages")
def messages() -> list[dict]:
    try:
        with psycopg.connect(_dsn(), connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, body, created_at FROM messages ORDER BY id")
                rows = cur.fetchall()
    except KeyError as exc:
        raise HTTPException(status_code=500, detail=f"missing credential: {exc}") from exc
    except psycopg.OperationalError as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return [
        {"id": row[0], "body": row[1], "created_at": row[2].isoformat()}
        for row in rows
    ]

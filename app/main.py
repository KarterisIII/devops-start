import os
import psycopg

from fastapi import FastAPI

app = FastAPI()


def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "devops_start"),
        user=os.getenv("DB_USER", "devops_user"),
        password=os.getenv("DB_PASSWORD", "devops_pass"),
    )


@app.get("/")
def root():
    return {"message": "DevOps start"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/dbcheck")
def dbcheck():
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                result = cur.fetchone()

        return {"database": "ok", "result": result[0]}
    except Exception as e:
        return {"database": "error", "details": str(e)}

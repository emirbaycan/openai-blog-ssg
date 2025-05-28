import os
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", 5432),
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
    )

def fetch_one_title_to_process():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title FROM blog_creation_queue_blogcreationqueue
                WHERE processed = FALSE
                ORDER BY created_at ASC
                LIMIT 1
            """)
            row = cur.fetchone()
    conn.close()
    return row  

def dispatch_one_job():
    job = fetch_one_title_to_process()
    if not job:
        print("No unprocessed titles found.")
        return
    title_id, title = job
    try:
        resp = requests.post(
            "http://ai:5000/generate/",
            json={"title_id": title_id},
            timeout=300
        )
        print(f"[{title_id}] {title} -> Status: {resp.status_code}, Response: {resp.text}")
    except Exception as e:
        print(f"[{title_id}] {title} -> Hata: {e}")

if __name__ == "__main__":
    dispatch_one_job()

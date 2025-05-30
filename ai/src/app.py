import os
import psycopg2
from src.agents.blogpostcreator import BlogPostCreator
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

def ping_search_engines(sitemap_url):
    engines = [
        f"https://www.google.com/ping?sitemap={sitemap_url}",
        f"https://www.bing.com/ping?sitemap={sitemap_url}",
        f"https://webmaster.yandex.com/ping?sitemap={sitemap_url}",
    ]
    for url in engines:
        try:
            resp = requests.get(url, timeout=5)
            print(f"[*] Pinged: {url} - Status: {resp.status_code}")
        except Exception as e:
            print(f"[!] Ping error: {url} - {e}")


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", 5432),
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
    )

def fetch_title_by_id(title_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title FROM blog_creation_queue_blogcreationqueue
                WHERE id = %s
            """, (title_id,))
            row = cur.fetchone()
    conn.close()
    return row  # (id, title)

def mark_title_as_processed(title_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE blog_creation_queue_blogcreationqueue
                SET processed = TRUE, processed_at = NOW()
                WHERE id = %s
            """, (title_id,))
    conn.close()

import subprocess

def run_ursus():
    try:
        result = subprocess.run(
            ["python", "/app/bin/ursus"],
            cwd="/app",
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("[!] Ursus error:")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
        print("Exception:", e)

def process_title(title_id, web_references=3):
    row = fetch_title_by_id(title_id)
    if not row:
        print(f"[!] No title found with id={title_id}")
        return

    _, title = row
    print(f"[*] Generating for: {title} (id={title_id})")
    creator = BlogPostCreator(title, web_references)
    try:
        filepath = creator.create_blog_post()
        if not filepath or isinstance(filepath, Exception):
            print(f"[!] Failed to generate for: {title} -- {filepath}")
            return
        print(f"[*] Saved: {filepath}")
        mark_title_as_processed(title_id)

        print("[*] Running Ursus static site generator...")
        try:
            run_ursus()
            print("[*] Ursus completed.")
            sitemap_url = "https://blog.emirbaycan.com.tr/sitemap.xml"
            ping_search_engines(sitemap_url)
            print("[*] Search engines notified.")
        except Exception as e:
            print(f"[!] Ursus error: {e}")

    except Exception as e:
        print(f"[!] Exception for {title}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python app.py <title_id>")
        sys.exit(1)
    title_id = int(sys.argv[1])
    process_title(title_id)

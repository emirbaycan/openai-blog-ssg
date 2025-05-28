import os
from agents.blogpostcreator import BlogPostCreator
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent / ".env")

def generate_blogs_from_titles(titles_path, web_references=3):
    titles_file = Path(titles_path)
    if not titles_file.exists():
        print(f"Titles file not found: {titles_file}")
        return
  
    with open(titles_file, "r", encoding="utf-8") as f:
        titles = [line.strip() for line in f if line.strip()]

    for title in titles:
        print(f"[*] Generating for: {title}")
        creator = BlogPostCreator(title, web_references)
        try:
            filepath = creator.create_blog_post()
            if not filepath or isinstance(filepath, Exception):
                print(f"[!] Failed to generate for: {title} -- {filepath}")
                continue
            print(f"[*] Saved: {filepath}")
        except Exception as e:
            print(f"[!] Exception for {title}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python app.py <titles.txt>")
        sys.exit(1)
    titles_path = sys.argv[1]
    generate_blogs_from_titles(titles_path)

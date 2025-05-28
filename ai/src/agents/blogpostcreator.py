import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import openai

from agents.prompts import BLOG_CREATOR_PROMPT
from agents.process_blog_post import extract_description_and_tags

import psycopg2

load_dotenv()  # .env'den OPENAI_API_KEY alınır

FRONTEND_BLOG_DIR = Path(__file__).parent.parent.parent.parent / "frontend" / "content" / "blog"

def sanitize_filename(title):
    # Türkçe karakter dönüşüm tablosu
    tr_map = str.maketrans(
        "ğüşıöçĞÜŞİÖÇ",
        "gusiocGUSIOC"
    )
    name = title.translate(tr_map).lower()
    name = re.sub(r'[^a-z0-9\-_. ]+', '', name)
    name = name.replace(" ", "-")
    return name[:48] + ".md"  # Çok uzun başlıkları kes

def get_or_create_tag(conn, tag_name):
    cur = conn.cursor()
    # Tag’i bulmaya çalış
    cur.execute("SELECT id FROM tag_tag WHERE name = %s", (tag_name,))
    result = cur.fetchone()
    if result:
        tag_id = result[0]
    else:
        # Yoksa ekle
        cur.execute("INSERT INTO tag_tag (name) VALUES (%s) RETURNING id", (tag_name,))
        tag_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    return tag_id

def get_ai_bot_user_id(conn, username="ai-bot"):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM auth_user WHERE username = %s", (username,))
        row = cur.fetchone()
    if row:
        return row[0]
    raise ValueError(f"User '{username}' not found in auth_user table.")

def insert_post_to_db(title, content, description, tags):
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", 5432),
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
    )
    
    author_id = get_ai_bot_user_id(conn, "ai-bot") 
    
    tag_id = None
    if tags and len(tags) > 0:
        tag_id = get_or_create_tag(conn, tags[0]) 
    pub_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO post_post (title, content, content_preview, pub_date, author_id, is_index_post, tag_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (title, content, description, pub_date, author_id, False, tag_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"[INFO] Post inserted into database: {title} (tag: {tags[0] if tag_id else None})")
    
    
class BlogPostCreator:
    def __init__(self, keyword, number_of_web_references=3):
        self.keyword = keyword
        self.number_of_web_references = int(number_of_web_references)
        # DOĞRU YÖNTEM: Client değil, sadece api_key'i ayarla!
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def serpapi_search(self, query, num=None):
        if num is None:
            num = self.number_of_web_references
        api_key = os.environ.get("SERP_API_KEY")
        url = f"https://serpapi.com/search.json?q={requests.utils.quote(query)}&engine=duckduckgo&api_key={api_key}"
        resp = requests.get(url)
        data = resp.json()
        links = []
        if 'organic_results' in data:
            for result in data['organic_results'][:num]:
                if result.get('link'):
                    links.append(result.get('link'))
        return links

    def fetch_web_content(self, url):
        try:
            print(f"[INFO] Fetching: {url}")
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            tags = soup.find_all(['p', 'h1', 'h2', 'h3'])
            texts = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True)]
            page_text = "\n".join(texts[:20])
            if not page_text:
                print(f"[WARN] No text found at: {url}")
            return page_text
        except Exception as e:
            print(f"[ERROR] Error fetching {url}: {e}")
            return ""

    def save_markdown(self, title, body, tags=None, description=None):
        # Oto doldurma
        if description is None or not description.strip() or description.startswith("Auto-generated"):
            description, _ = extract_description_and_tags(body)
        if not tags or tags == ["ai", "auto"]:
            _, tags = extract_description_and_tags(body)

        filename = sanitize_filename(title)
        directory = FRONTEND_BLOG_DIR
        os.makedirs(directory, exist_ok=True)
        filepath = directory / filename
        frontmatter = f"""---
            title: {title}
            description: {description}
            date_created: {datetime.now().strftime('%Y-%m-%d')}
            tags: {tags}
            ---

            {body}
        """
        with open(filepath, 'w', encoding="utf-8") as f:
            f.write(frontmatter)
            
        insert_post_to_db(title, body, description, tags)
        
        print(f"[SUCCESS] File saved as {filepath}")
        return filepath

    def create_blog_post(self):
        print(f"[INFO] Creating blog post for: {self.keyword}")
        links = self.serpapi_search(self.keyword)
        if not links:
            print("[WARN] No links found.")
            return None

        context = ""
        for link in links:
            page_text = self.fetch_web_content(link)
            if page_text:
                context += page_text + "\n\n"
        if not context:
            print("[WARN] No context found in fetched links.")
            return None

        full_prompt = BLOG_CREATOR_PROMPT.format(
            keyword=self.keyword,
            context=context
        )

        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.8,
                max_tokens=4000,
            )
            blog_content = response.choices[0].message.content
            if not blog_content:
                print("[WARN] AI returned empty content.")
                return None
            
            
            return self.save_markdown(
                title=self.keyword,
                body=blog_content,
                tags=["ai", "auto"],
                description=f"{self.keyword}"
            )
        except Exception as e:
            print(f"[ERROR] OpenAI error: {e}")
            return None

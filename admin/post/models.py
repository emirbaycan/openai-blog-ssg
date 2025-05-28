from django.contrib.auth.models import User
from django.db import models
from mdeditor.fields import MDTextField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from tag.models import Tag
from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BLOG_DIR = BASE_DIR / "frontend" / "content" / "blog"

def sanitize_filename(title):
    title = title.lower()
    title = (title
        .replace("ç", "c").replace("ğ", "g").replace("ı", "i")
        .replace("ö", "o").replace("ş", "s").replace("ü", "u")
    )
    title = re.sub(r'[^\w\-_. ]+', '', title)
    title = title.replace(" ", "-")
    return title[:48] + ".md"

def get_markdown_filepath(post):
    filename = sanitize_filename(post.title)
    return BLOG_DIR / filename

def post_to_markdown(post):
    content = post.content or ""
    match = re.search(r'(?:^|\n)([^\n]+)\n', content)
    description = match.group(1).strip() if match else ""
    tags = [post.tag.name] if post.tag else []

    frontmatter = f"""---
        title: {post.title}
        description: {description}
        date_created: {post.pub_date.strftime('%Y-%m-%d')}
        tags: {tags}
        ---

        {content}
    """
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    filepath = get_markdown_filepath(post)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(frontmatter)
    print(f"[INFO] Exported to: {filepath}")

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = MDTextField(null=True, blank=True)
    content_preview = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_index_post = models.BooleanField(default=False)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=False)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        post_to_markdown(self)

class TextAsset(models.Model):
    ASSET_TYPES = (
        ('logo', 'Logo'),
        ('copyright', 'Copyright'),
        ('about', 'About'),
        ('contact', 'Contact')
    )
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    content = models.TextField()

    def __str__(self):
        return f"{self.get_asset_type_display()}: {self.content[:50]}"

@receiver(post_delete, sender=Post)
def delete_markdown_on_post_delete(sender, instance, **kwargs):
    md_path = get_markdown_filepath(instance)
    if md_path.exists():
        md_path.unlink()
        print(f"[INFO] Deleted markdown: {md_path}")
    else:
        print(f"[INFO] No markdown found for deleted post: {md_path}")

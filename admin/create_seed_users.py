import os
import django
from django.contrib.auth import get_user_model
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(str(BASE_DIR / ".env"))  # .env yolunu doğrula

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
django.setup()

User = get_user_model()

def create_superuser():
    superuser_username = env("DJANGO_SUPERUSER_USERNAME", default="admin")
    superuser_email = env("DJANGO_SUPERUSER_EMAIL", default="admin@example.com")
    superuser_password = env("DJANGO_SUPERUSER_PASSWORD", default="adminpass")
    if not User.objects.filter(username=superuser_username).exists():
        print(f"Creating superuser: {superuser_username}")
        User.objects.create_superuser(username=superuser_username, email=superuser_email, password=superuser_password)
    else:
        print(f"Superuser '{superuser_username}' already exists.")

def create_ai_user():
    ai_username = env("DJANGO_AI_BOT_USERNAME", default="ai-bot")
    ai_email = env("DJANGO_AI_BOT_EMAIL", default="ai-bot@yourdomain.com")
    ai_password = env("DJANGO_AI_BOT_PASSWORD", default="defaultpassword")
    if not User.objects.filter(username=ai_username).exists():
        user = User.objects.create_user(username=ai_username, email=ai_email, password=ai_password)
        user.is_active = True
        user.is_staff = False
        user.save()
        print(f"Created AI bot user: {ai_username}")
    else:
        print(f"AI bot user '{ai_username}' already exists.")

if __name__ == "__main__":
    create_superuser()
    create_ai_user()

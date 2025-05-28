import os
import django
from django.contrib.auth import get_user_model
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(str(BASE_DIR / ".env"))  # Adjust path if .env location differs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
django.setup()

User = get_user_model()

username = env("DJANGO_SUPERUSER_USERNAME", default="admin")
email = env("DJANGO_SUPERUSER_EMAIL", default="admin@example.com")
password = env("DJANGO_SUPERUSER_PASSWORD", default="adminpass")

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser: {username}")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print(f"Superuser {username} already exists")

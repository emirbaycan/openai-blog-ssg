import re
from collections import Counter

TURKISH_STOPWORDS = set([
    "ve", "bir", "bu", "ile", "de", "da", "için", "ama", "ya", "en", "çok", "daha",
    "ki", "mi", "ben", "sen", "o", "biz", "siz", "onlar", "ne", "neden", "nasıl",
    "the", "and", "to", "of", "a", "in", "on", "is", "it", "as", "at", "by", "an", "from",
])

def extract_first_paragraph(body):
    lines = [line.strip() for line in body.splitlines()]
    lines = [l for l in lines if not l.startswith('#') and not l.startswith('---') and l]
    for line in lines:
        if len(line) > 20: 
            return line
    return lines[0] if lines else ""

def extract_first_sentence(text):
    # İlk . işaretine kadar olan kısmı döndür
    return text.split('.', 1)[0].strip() + '.'

def extract_top_keywords(body, n=5):
    cleaned = re.sub(r'[^\w\s]', ' ', body.lower())
    cleaned = re.sub(r'\d+', '', cleaned)
    words = cleaned.split()
    words = [w for w in words if w not in TURKISH_STOPWORDS and len(w) > 2]
    most_common = Counter(words).most_common(n)
    return [w for w, _ in most_common]

def extract_description_and_tags(body):
    description = extract_first_paragraph(body)
    description = extract_first_sentence(description)
    tags = extract_top_keywords(body, n=5)
    return description, tags

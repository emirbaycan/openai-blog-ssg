import os
from datetime import datetime

def generate_sitemap(output_dir, base_url):
    sitemap_path = os.path.join(output_dir, 'sitemap.xml')
    urls = []

    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith('.html'):
                rel_path = os.path.relpath(os.path.join(root, file), output_dir)
                url = os.path.join(base_url, rel_path.replace(os.path.sep, '/'))
                if url.endswith('index.html'):
                    url = url[:-10]  # Remove 'index.html'
                urls.append(url)

    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in urls:
            f.write('  <url>\n')
            f.write(f'    <loc>{url}</loc>\n')
            f.write(f'    <lastmod>{datetime.utcnow().date()}</lastmod>\n')
            f.write('    <changefreq>weekly</changefreq>\n')
            f.write('    <priority>0.8</priority>\n')
            f.write('  </url>\n')
        f.write('</urlset>\n')
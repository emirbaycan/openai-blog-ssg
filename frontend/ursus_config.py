from datetime import datetime
from pathlib import Path
from ursus.config import config
import logging
import os
from ursus.context_processors import get_entries

config.content_path = Path(__file__).parent / 'content'
config.templates_path = Path(__file__).parent / 'templates'
config.output_path = Path(__file__).parent.parent / 'output'

config.site_url = os.environ.get('site_url', 'https://blog.emirbaycan.com.tr')
config.html_url_extension = ''
config.minify_js = True
config.minify_css = True

config.context_processors.append('ursus.context_processors.git_date.GitDateProcessor')

# Önce mevcut global'leri al
default_globals = getattr(config, "context_globals", {})

config.context_globals = {
    **default_globals,
    'now': datetime.now(),
    'site_url': 'https://blog.emirbaycan.com.tr',
    'is_golden': lambda uri, entry: 'golden' in entry.get('categories', []),
    'is_not_golden': lambda uri, entry: 'golden' not in entry.get('categories', []),
}

config.image_transforms = {
    '': {
        'include': ('files/*.pdf', ),
        'output_types': ('original', ),
    },
    'content2x': {
        'exclude': ('*.pdf', '*.svg'),
        'max_size': (1848, 1848),
        'output_types': ('original', 'webp'),
    },
    'content1x': {
        'exclude': ('*.pdf', '*.svg'),
        'max_size': (924, 924),
        'output_types': ('original', 'webp'),
    },
    'content0.75x': {
        'exclude': ('*.pdf', '*.svg'),
        'max_size': (690, 690),
        'output_types': ('original', 'webp'),
    },
}

config.linters = [
    'ursus.linters.footnotes.OrphanFootnotesLinter',
    'ursus.linters.images.UnusedImagesLinter',
    'ursus.linters.markdown.MarkdownInternalLinksLinter',
    'ursus.linters.markdown.MarkdownLinkTextsLinter',
    'ursus.linters.markdown.MarkdownLinkTitlesLinter',
    'ursus.linters.markdown.RelatedEntriesLinter',
]

config.logging = {
    'level': logging.INFO,
    'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)d] %(message)s',
}

config.add_markdown_extension('nl2br')

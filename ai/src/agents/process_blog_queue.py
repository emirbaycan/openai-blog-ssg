from django.core.management.base import BaseCommand
from blog_creation_queue.models import BlogCreationQueue

class Command(BaseCommand):
    help = 'Pushes first unprocessed blog title to ai/titles.txt for AI processing'

    def handle(self, *args, **options):
        entry = BlogCreationQueue.objects.filter(processed=False).order_by('created_at').first()
        if entry:
            with open('ai/titles.txt', 'w', encoding='utf-8') as f:
                f.write(entry.title + '\n')
            self.stdout.write(self.style.SUCCESS(f'Pushed "{entry.title}" to titles.txt'))
        else:
            self.stdout.write('No unprocessed titles found.')

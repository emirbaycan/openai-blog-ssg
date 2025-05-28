from django.contrib import admin
from blog_creation_queue.models import BlogCreationQueue
import requests

@admin.register(BlogCreationQueue)
class BlogCreationQueueAdmin(admin.ModelAdmin):
    list_display = ('title', 'processed', 'created_at', 'processed_at')
    list_filter = ('processed',)
    search_fields = ('title',)
    ordering = ('-created_at',)
    actions = ['mark_as_processed', 'process_with_ai']

    @admin.action(description="Seçili başlıkları işlenmiş olarak işaretle")
    def mark_as_processed(self, request, queryset):
        queryset.update(processed=True)

    @admin.action(description="AI ile seçili başlıkları oluştur")
    def process_with_ai(self, request, queryset):
        successes = 0
        errors = []
        for entry in queryset:
            try:
                resp = requests.post(
                    "http://ai:5000/generate/", 
                    json={"title_id": entry.id},
                    timeout=60
                )
                if resp.ok:
                    successes += 1
                else:
                    errors.append(f"{entry.title} (id={entry.id}): {resp.text}")
            except Exception as e:
                errors.append(f"{entry.title} (id={entry.id}): {e}")

        msg = f"AI işleme başlatıldı: {successes} başlık."
        if errors:
            msg += f" Hatalı olanlar: {len(errors)}\n" + "\n".join(errors)
        self.message_user(request, msg)

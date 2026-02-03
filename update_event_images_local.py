#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from event.models import Event

# Map event titles to local frontend asset paths
# These will be served from the Vite dev server
event_images = {
    'Everest Base Camp Trek': '/src/assets/imgs/Everest.jpg',
    'Annapurna Circuit Adventure': '/src/assets/imgs/Manang.jpg',
    'Kathmandu Cultural Tour': '/src/assets/imgs/Kathmandu.jpg',
    'Chitwan Wildlife Safari': '/src/assets/imgs/image-01.jpg',
    'Pokhara Paragliding Experience': '/src/assets/imgs/Pokhara.jpg',
    'Lumbini Pilgrimage Tour': '/src/assets/imgs/Lumbini .jpg',
}

print("📸 Updating events with local images...\n")

for title, image_path in event_images.items():
    try:
        event = Event.objects.get(title=title)
        event.image = image_path
        event.save()
        print(f"✅ Updated: {title} -> {image_path}")
    except Event.DoesNotExist:
        print(f"⚠️  Event not found: {title}")

print(f"\n🎉 Local images assigned successfully!")
print(f"📊 Total events: {Event.objects.count()}")

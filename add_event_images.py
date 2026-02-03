#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from event.models import Event

# Map event titles to Unsplash image URLs (royalty-free)
event_images = {
    'Everest Base Camp Trek': 'https://images.unsplash.com/photo-1486870591958-9b9d0d1dda99?w=800',
    'Annapurna Circuit Adventure': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
    'Kathmandu Cultural Tour': 'https://images.unsplash.com/photo-1558005530-a7958896ec60?w=800',
    'Chitwan Wildlife Safari': 'https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=800',
    'Pokhara Paragliding Experience': 'https://images.unsplash.com/photo-1483479423850-e1a6bce2c0e7?w=800',
    'Lumbini Pilgrimage Tour': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800',
}

print("📸 Adding images to events...\n")

for title, image_url in event_images.items():
    try:
        event = Event.objects.get(title=title)
        # Store the URL directly in the image field as a string
        # Note: This is a workaround since we don't have actual image files
        event.image = image_url
        event.save()
        print(f"✅ Updated: {title}")
    except Event.DoesNotExist:
        print(f"⚠️  Event not found: {title}")

print(f"\n🎉 Image URLs added successfully!")
print(f"📊 Total events: {Event.objects.count()}")

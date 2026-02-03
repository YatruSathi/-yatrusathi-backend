#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from event.models import Event

# Get admin user
admin = User.objects.get(username='admin')

# Sample events data
events_data = [
    {
        'title': 'Everest Base Camp Trek',
        'description': 'Join us for an unforgettable journey to Everest Base Camp. Experience breathtaking mountain views and immerse yourself in Sherpa culture.',
        'location': 'Everest Region, Nepal',
        'date': datetime.now() + timedelta(days=30),
    },
    {
        'title': 'Annapurna Circuit Adventure',
        'description': 'A classic trek through diverse landscapes, from lush subtropical forests to high mountain passes. Perfect for adventure seekers!',
        'location': 'Annapurna Region, Nepal',
        'date': datetime.now() + timedelta(days=45),
    },
    {
        'title': 'Kathmandu Cultural Tour',
        'description': 'Explore the rich cultural heritage of Kathmandu Valley. Visit ancient temples, palaces, and UNESCO World Heritage sites.',
        'location': 'Kathmandu Valley, Nepal',
        'date': datetime.now() + timedelta(days=15),
    },
    {
        'title': 'Chitwan Wildlife Safari',
        'description': 'Experience the wildlife of Chitwan National Park. Spot rhinos, tigers, and exotic birds in their natural habitat.',
        'location': 'Chitwan National Park, Nepal',
        'date': datetime.now() + timedelta(days=20),
    },
    {
        'title': 'Pokhara Paragliding Experience',
        'description': 'Soar above the beautiful Pokhara valley with stunning views of Phewa Lake and the Annapurna range.',
        'location': 'Pokhara, Nepal',
        'date': datetime.now() + timedelta(days=10),
    },
    {
        'title': 'Lumbini Pilgrimage Tour',
        'description': 'Visit the birthplace of Lord Buddha. A spiritual journey through sacred gardens and ancient monasteries.',
        'location': 'Lumbini, Nepal',
        'date': datetime.now() + timedelta(days=25),
    },
]

# Create events
created_count = 0
for event_data in events_data:
    event, created = Event.objects.get_or_create(
        title=event_data['title'],
        defaults={
            'description': event_data['description'],
            'location': event_data['location'],
            'date': event_data['date'],
            'created_by': admin,
        }
    )
    if created:
        created_count += 1
        print(f"✅ Created: {event.title}")
    else:
        print(f"⚠️  Already exists: {event.title}")

print(f"\n🎉 Successfully created {created_count} new events!")
print(f"📊 Total events in database: {Event.objects.count()}")

import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from event.models import Event, Profile, Booking, Review, Notification

def populate_db():
    print("Starting database population...")

    # 1. Create Users
    usernames = ['trekker_nepal', 'adventure_seeker', 'culture_buff', 'himalayan_guide', 'travel_guru']
    users = []
    for uname in usernames:
        user, created = User.objects.get_or_create(
            username=uname,
            defaults={
                'email': f"{uname}@example.com",
                'first_name': uname.split('_')[0].capitalize(),
                'last_name': uname.split('_')[1].capitalize() if '_' in uname else 'User'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            Profile.objects.get_or_create(user=user, defaults={'bio': f"Hi, I'm {user.first_name}, a passionate traveler exploring Nepal!"})
        users.append(user)

    # Admin user
    admin_user = User.objects.get(username='admin')

    # 2. Sample Data for Events
    event_data = [
        {
            'title': 'Annapurna Circuit Expedition',
            'description': 'A legendary trek through the heart of the Himalayas. Experience diverse landscapes, from lush sub-tropical forests to alpine meadows and high-altitude deserts.',
            'category': 'Trekking',
            'location': 'Annapurna Region',
            'image': '/assets/imgs/Manang.jpg',
            'tags': 'Adventure, Trekking, Mountains',
            'ticket_price': 1200.00,
            'organizer_name': 'Himalayan Adventures'
        },
        {
            'title': 'Kathmandu Heritage Walk',
            'description': 'Explore the ancient temples, stupas, and palaces of the Kathmandu Valley. A journey through centuries of art, culture, and spirituality.',
            'category': 'Cultural',
            'location': 'Kathmandu',
            'image': '/assets/imgs/Lumbini .jpg',
            'tags': 'Culture, History, Temples',
            'ticket_price': 45.00,
            'organizer_name': 'Heritage Nepal'
        },
        {
            'title': 'Chitwan Wildlife Safari',
            'description': 'Get close to one-horned rhinos, Bengal tigers, and diverse bird species in the lush jungles of Chitwan National Park.',
            'category': 'Wildlife',
            'location': 'Chitwan',
            'image': 'https://images.unsplash.com/photo-1581260466152-d2c0303e54f5?q=80&w=2000',
            'tags': 'Nature, Animals, Safari',
            'ticket_price': 150.00,
            'organizer_name': 'Jungle Trails'
        },
        {
            'title': 'Pokhara Paragliding Adventure',
            'description': 'Soar high above the Phewa Lake with stunning views of the Annapurna massif. An adrenaline-pumping experience like no other.',
            'category': 'Adventure',
            'location': 'Pokhara',
            'image': 'https://images.unsplash.com/photo-1544735038-179ad9678e24?q=80&w=2000',
            'tags': 'Adventure, Flying, Adrenaline',
            'ticket_price': 85.00,
            'organizer_name': 'Sky High Pokhara'
        },
        {
            'title': 'Everest Base Camp Luxury Trek',
            'description': 'The ultimate bucket list adventure with a touch of comfort. See the world\'s highest peak up close while staying in the best lodges available.',
            'category': 'Trekking',
            'location': 'Everest Region',
            'image': '/assets/imgs/Everest.jpg',
            'tags': 'Everest, Luxury, Trekking',
            'ticket_price': 2500.00,
            'organizer_name': 'Peak Pursuits'
        },
        {
            'title': 'Lumbini Peace Pilgrimage',
            'description': 'Visit the birthplace of Lord Buddha and find inner peace among the monastic zones and sacred gardens.',
            'category': 'Cultural',
            'location': 'Lumbini',
            'image': '/assets/imgs/Lumbini .jpg',
            'tags': 'Spirituality, Peace, Buddhism',
            'ticket_price': 0.00,
            'organizer_name': 'Spiritual Nepal'
        }
    ]

    # Create 15 more events for variety
    more_locations = ['Mustang', 'Gorkha', 'Bandipur', 'Nagarkot', 'Dhulikhel']
    more_titles = ['Mountain Biking', 'Yoga Retreat', 'Food Tour', 'Photography Workshop', 'Village Homestay']
    
    for i in range(14):
        title = f"{random.choice(more_locations)} {random.choice(more_titles)}"
        event_data.append({
            'title': title,
            'description': f"An amazing {title} experience that you will never forget. Join us for a unique journey into the heart of Nepal.",
            'category': random.choice(['Adventure', 'Cultural', 'Trekking', 'Wildlife', 'Music']),
            'location': random.choice(more_locations),
            'image': f"https://images.unsplash.com/photo-{1500000000000 + i}?q=80&w=2000",
            'tags': 'Nepal, Travel, Experience',
            'ticket_price': random.randint(20, 500),
            'organizer_name': 'Local Nepal Guides'
        })

    created_events = []
    for data in event_data:
        event, created = Event.objects.get_or_create(
            title=data['title'],
            defaults={
                'description': data['description'],
                'category': data['category'],
                'location': data['location'],
                'image': data['image'],
                'tags': data['tags'],
                'ticket_price': data['ticket_price'],
                'is_free_event': data['ticket_price'] == 0,
                'organizer_name': data['organizer_name'],
                'date': timezone.now() + timedelta(days=random.randint(5, 60)),
                'created_by': admin_user
            }
        )
        created_events.append(event)

    # 3. Create Bookings, Reviews, and Notifications
    for user in users:
        # Each user books 2-4 events
        for event in random.sample(created_events, k=random.randint(2, 4)):
            Booking.objects.get_or_create(
                user=user,
                event=event,
                defaults={'status': 'confirmed', 'ticket_count': random.randint(1, 3)}
            )
            # Add review for some events
            if random.random() > 0.5:
                Review.objects.get_or_create(
                    user=user,
                    event=event,
                    defaults={
                        'rating': random.randint(4, 5),
                        'comment': f"Amazing experience! {event.title} was definitely worth it. Highly recommend to everyone visiting Nepal."
                    }
                )
            # Add notification
            Notification.objects.create(
                user=user,
                message=f"Your booking for {event.title} has been confirmed. Get ready for the adventure!",
                is_read=random.choice([True, False])
            )

    print(f"Successfully created {len(created_events)} events, {len(users)} users, and their associated data.")

if __name__ == "__main__":
    populate_db()

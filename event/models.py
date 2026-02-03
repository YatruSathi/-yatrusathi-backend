from django.db import models
from django.contrib.auth.models import User

# ----------------------------
# Event Model
# ----------------------------
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    
    # Advanced fields for professional look
    tags = models.CharField(max_length=255, blank=True, null=True)
    start_date_time = models.DateTimeField(blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    map_link = models.URLField(max_length=500, blank=True, null=True)
    min_participants = models.IntegerField(default=1)
    max_participants = models.IntegerField(blank=True, null=True)
    gender_preference = models.CharField(
        max_length=20, 
        choices=[('any', 'Any'), ('male', 'Male Only'), ('female', 'Female Only')], 
        default='any'
    )
    age_limit = models.IntegerField(blank=True, null=True)
    prior_experience_required = models.BooleanField(default=False)
    is_free_event = models.BooleanField(default=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pay_on_site = models.BooleanField(default=False)
    equipment_list = models.TextField(blank=True, null=True)
    organizer_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    social_media_link = models.URLField(max_length=500, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    participants = models.ManyToManyField(User, related_name='events_participating', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='event_gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.event.title}"


# ----------------------------
# Notification Model
# ----------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:20]}"


# ----------------------------
# ChatMessage Model
# ----------------------------
class ChatMessage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:20]}"


# ----------------------------
# Favorite Model
# ----------------------------
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} likes {self.event.title}"


# ----------------------------
# Profile Model
# ----------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    
    # KYC Fields
    full_name = models.CharField(max_length=255, blank=True)
    citizenship_number = models.CharField(max_length=50, blank=True)
    document_image = models.ImageField(upload_to='kyc_docs/', blank=True, null=True)
    is_kyc_verified = models.BooleanField(default=False)
    kyc_submitted_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"


# ----------------------------
# Booking Model
# ----------------------------
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    ticket_count = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


# ----------------------------
# Review Model
# ----------------------------
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.event.title}"

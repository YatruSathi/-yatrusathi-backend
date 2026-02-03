from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Notification, ChatMessage, Favorite, Profile, Booking, Review, EventImage

# ----------------------------
# User Serializer
# ----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ----------------------------
# Profile Serializer
# ----------------------------
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'name', 'email', 'bio', 'hobbies', 'avatar', 'phone', 'location',
            'full_name', 'citizenship_number', 'document_image', 'is_kyc_verified', 'kyc_submitted_at'
        ]
        read_only_fields = ['is_kyc_verified', 'kyc_submitted_at']

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ['id', 'image', 'created_at']

# ----------------------------
# Event Serializer
# ----------------------------
class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    images = EventImageSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'location', 'category', 'image',
            'tags', 'start_date_time', 'end_date_time', 'location_name', 'map_link',
            'min_participants', 'max_participants', 'gender_preference', 'age_limit', 'prior_experience_required',
            'is_free_event', 'ticket_price', 'pay_on_site', 'equipment_list',
            'organizer_name', 'contact_email', 'phone_number', 'social_media_link',
            'created_by', 'participants', 'images', 'created_at', 'updated_at'
        ]

# ----------------------------
# Booking Serializer
# ----------------------------
class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source='event',
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'event_id', 'booked_at', 'status', 'ticket_count']

# ----------------------------
# Review Serializer
# ----------------------------
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'event', 'rating', 'comment', 'created_at']

# ----------------------------
# Notification Serializer
# ----------------------------
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']

# ----------------------------
# ChatMessage Serializer
# ----------------------------
class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'event', 'sender', 'message', 'timestamp']

# ----------------------------
# Favorite Serializer
# ----------------------------
class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source='event',
        write_only=True
    )

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'event', 'event_id', 'created_at']

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Notification, ChatMessage, Favorite, Profile

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

    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'avatar']

# ----------------------------
# Event Serializer
# ----------------------------
class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'created_by', 'participants', 'created_at', 'updated_at']

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

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'event', 'created_at']

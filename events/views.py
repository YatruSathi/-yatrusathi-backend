from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Event, Notification, ChatMessage, Favorite, Profile
from .serializers import (
	ProfileSerializer, EventSerializer, NotificationSerializer,
	ChatMessageSerializer, FavoriteSerializer, UserSerializer
)

# Event Views
class EventListCreateView(generics.ListCreateAPIView):
	queryset = Event.objects.all().order_by('-date')
	serializer_class = EventSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Notification Views
class NotificationListView(generics.ListAPIView):
	serializer_class = NotificationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Notification.objects.filter(user=self.request.user).order_by('-created_at')

# ChatMessage Views
class ChatMessageListCreateView(generics.ListCreateAPIView):
	serializer_class = ChatMessageSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		event_id = self.kwargs.get('event_id')
		return ChatMessage.objects.filter(event_id=event_id).order_by('timestamp')

	def perform_create(self, serializer):
		event_id = self.kwargs.get('event_id')
		serializer.save(sender=self.request.user, event_id=event_id)

# Favorite Views
class FavoriteListCreateView(generics.ListCreateAPIView):
	serializer_class = FavoriteSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Favorite.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

# Profile Views
class ProfileDetailView(generics.RetrieveUpdateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return Profile.objects.get(user=self.request.user)

# User List (for reference, e.g. participants)
class UserListView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
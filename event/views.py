from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Event, Notification, ChatMessage, Favorite, Profile, Booking, Review
from .serializers import (
	ProfileSerializer, EventSerializer, NotificationSerializer,
	ChatMessageSerializer, FavoriteSerializer, UserSerializer,
	BookingSerializer, ReviewSerializer
)

# Authentication Views
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
	"""
	Login endpoint that accepts email and password
	Returns authentication token and user data
	"""
	email = request.data.get('email')
	password = request.data.get('password')
	
	if not email or not password:
		return Response(
			{'message': 'Email and password are required'},
			status=status.HTTP_400_BAD_REQUEST
		)
	
	# Try to get user by email
	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		return Response(
			{'message': 'Invalid email or password'},
			status=status.HTTP_401_UNAUTHORIZED
		)
	
	# Authenticate with username and password
	authenticated_user = authenticate(username=user.username, password=password)
	
	if authenticated_user is None:
		return Response(
			{'message': 'Invalid email or password'},
			status=status.HTTP_401_UNAUTHORIZED
		)
	
	# Get or create token
	token, created = Token.objects.get_or_create(user=authenticated_user)
	
	# Get or create profile
	profile, _ = Profile.objects.get_or_create(user=authenticated_user)
	
	return Response({
		'token': token.key,
		'user': {
			'id': authenticated_user.id,
			'username': authenticated_user.username,
			'email': authenticated_user.email,
			'first_name': authenticated_user.first_name,
			'last_name': authenticated_user.last_name,
		}
	}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
	"""
	Logout endpoint that deletes the user's token
	"""
	try:
		request.user.auth_token.delete()
		return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
	except Exception as e:
		return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup_view(request):
	"""
	Signup endpoint that creates a new user
	Returns authentication token and user data
	"""
	username = request.data.get('username')
	email = request.data.get('email')
	password = request.data.get('password')
	first_name = request.data.get('first_name', '')
	last_name = request.data.get('last_name', '')
	
	if not username or not email or not password:
		return Response(
			{'message': 'Username, email, and password are required'},
			status=status.HTTP_400_BAD_REQUEST
		)
	
	# Check if username already exists
	if User.objects.filter(username=username).exists():
		return Response(
			{'message': 'Username already exists'},
			status=status.HTTP_400_BAD_REQUEST
		)
	
	# Check if email already exists
	if User.objects.filter(email=email).exists():
		return Response(
			{'message': 'Email already exists'},
			status=status.HTTP_400_BAD_REQUEST
		)
	
	try:
		# Create user
		user = User.objects.create_user(
			username=username,
			email=email,
			password=password,
			first_name=first_name,
			last_name=last_name
		)
		
		# Create token
		token = Token.objects.create(user=user)
		
		# Create profile
		Profile.objects.create(user=user)
		
		return Response({
			'token': token.key,
			'user': {
				'id': user.id,
				'username': user.username,
				'email': user.email,
				'first_name': user.first_name,
				'last_name': user.last_name,
			}
		}, status=status.HTTP_201_CREATED)
		
	except Exception as e:
		return Response(
			{'message': f'Error creating user: {str(e)}'},
			status=status.HTTP_500_INTERNAL_SERVER_ERROR
		)


# Custom Permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Custom permission to only allow creators of an object to edit it.
	"""
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		# Check if the object has an owner or creator field
		owner = getattr(obj, 'created_by', None) or getattr(obj, 'user', None) or getattr(obj, 'sender', None)
		return owner == request.user

# Event Views
class EventListCreateView(generics.ListCreateAPIView):
	queryset = Event.objects.all().order_by('-date')
	serializer_class = EventSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def perform_create(self, serializer):
		event = serializer.save(created_by=self.request.user)
		# Handle gallery images
		images = self.request.FILES.getlist('gallery_images')
		for image in images:
			EventImage.objects.create(event=event, image=image)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# Notification Views
class NotificationListView(generics.ListAPIView):
	serializer_class = NotificationSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Notification.objects.filter(user=self.request.user).order_by('-created_at')

# ChatMessage Views
class ChatMessageListCreateView(generics.ListCreateAPIView):
	serializer_class = ChatMessageSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

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
		# Prevent duplicate favorites
		event_id = self.request.data.get('event_id')
		if Favorite.objects.filter(user=self.request.user, event_id=event_id).exists():
			return
		serializer.save(user=self.request.user)

class FavoriteDetailView(generics.DestroyAPIView):
	queryset = Favorite.objects.all()
	serializer_class = FavoriteSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
	lookup_field = 'event_id'

	def get_object(self):
		event_id = self.kwargs.get('event_id')
		return Favorite.objects.get(user=self.request.user, event_id=event_id)

# Profile Views
class ProfileDetailView(generics.RetrieveUpdateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		profile, created = Profile.objects.get_or_create(user=self.request.user)
		return profile

# Booking Views
class BookingListCreateView(generics.ListCreateAPIView):
	serializer_class = BookingSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Booking.objects.filter(user=self.request.user)

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

# Review Views
class ReviewListCreateView(generics.ListCreateAPIView):
	serializer_class = ReviewSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		event_id = self.kwargs.get('event_id')
		if event_id:
			return Review.objects.filter(event_id=event_id)
		return Review.objects.all()

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

# User List (for reference, e.g. participants)
class UserListView(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/signup/', views.signup_view, name='signup'),

    # Event endpoints
    path('events/', views.EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),

    # Notification endpoints
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),

    # Chat endpoints (event-based chat)
    path('events/<int:event_id>/chat/', views.ChatMessageListCreateView.as_view(), name='chatmessage-list-create'),

    # Favorite endpoints
    path('favorites/', views.FavoriteListCreateView.as_view(), name='favorite-list-create'),
    path('favorites/<int:event_id>/', views.FavoriteDetailView.as_view(), name='favorite-detail'),

    # Profile endpoints
    path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),

    # Booking endpoints
    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list-create'),

    # Review endpoints
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list'),
    path('events/<int:event_id>/reviews/', views.ReviewListCreateView.as_view(), name='event-reviews'),

    # User list (for reference, e.g. participants)
    path('users/', views.UserListView.as_view(), name='user-list'),
]

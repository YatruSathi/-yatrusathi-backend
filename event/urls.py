from django.urls import path
from . import views

urlpatterns = [
    # Event endpoints
    path('events/', views.EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),

    # Notification endpoints
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),

    # Chat endpoints (event-based chat)
    path('events/<int:event_id>/chat/', views.ChatMessageListCreateView.as_view(), name='chatmessage-list-create'),

    # Favorite endpoints
    path('favorites/', views.FavoriteListCreateView.as_view(), name='favorite-list-create'),

    # Profile endpoints
    path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),

    # User list (for reference, e.g. participants)
    path('users/', views.UserListView.as_view(), name='user-list'),
]

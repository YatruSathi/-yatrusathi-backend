from django.contrib import admin
from .models import Event, ChatMessage, Notification, Profile, Favorite

# Register your models
admin.site.register(Event)
admin.site.register(ChatMessage)
admin.site.register(Notification)
admin.site.register(Profile)
admin.site.register(Favorite)

from django.contrib import admin
from .models import Event, ChatMessage, Notification, Profile, Favorite, Booking, Review

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'date', 'ticket_price', 'created_by')
    list_filter = ('category', 'date', 'created_by')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'phone')
    search_fields = ('user__username', 'user__email', 'location')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'booked_at')
    list_filter = ('status', 'booked_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

admin.site.register(ChatMessage)
admin.site.register(Notification)
admin.site.register(Favorite)

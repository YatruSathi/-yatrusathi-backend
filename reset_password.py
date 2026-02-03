#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Reset admin password
user = User.objects.get(username='admin')
user.set_password('admin123')
user.email = 'admin@example.com'
user.save()

print(f"✅ Password reset successfully!")
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Password: admin123")

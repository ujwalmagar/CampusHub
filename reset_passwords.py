import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

users = User.objects.all()
for u in users:
    u.set_password('password123')
    u.save()

print(f"Successfully reset passwords for {users.count()} users to 'password123'")

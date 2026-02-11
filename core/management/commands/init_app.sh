#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- 📦 Starting Media Initialization ---"

# 1. Collect all static files locally in the build
echo "Step 1: Collecting static files..."
python manage.py collectstatic --noinput

# 2. Organize seed media (copy images from static to media with correct folder structure)
echo "Step 2: Organizing seed media with correct folder structure..."
python manage.py load_seed_media

echo "--- ✅ Media Initialization Complete ---"

# 3. Create Superuser (Idempotent)
echo "Step 3: Checking for Admin User..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(username=username).exists():
    if password:
        User.objects.create_superuser(username, email, password)
        print(f"--- 👤 Superuser '{username}' created successfully ---")
    else:
        print("--- ⚠️ DJANGO_SUPERUSER_PASSWORD not set, skipping creation ---")
else:
    print(f"--- 👤 Superuser '{username}' already exists ---")
EOF

# 4. Start Gunicorn
echo "Step 4: Launching Gunicorn..."
exec gunicorn chambalabamba.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120

#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- 📦 Starting Media Initialization ---"

# 1. Collect all static files locally in the build
echo "Step 1: Collecting static files..."
python manage.py collectstatic --noinput

# 2. Define source and destination
SOURCE="staticfiles/"
DEST="/opt/render/project/src/media/"

# 3. Sync images and assets to the Persistent Disk
# We exclude code files and the admin dashboard assets
echo "Step 2: Syncing assets to Persistent Disk ($DEST)..."
rsync -rv --no-t --ignore-existing \
  --exclude='*.css' \
  --exclude='*.js' \
  --exclude='*.map' \
  --exclude='admin/' \
  --exclude='ckeditor/' \
  "$SOURCE" "$DEST"

echo "--- ✅ Media Initialization Complete ---"


# 4. Create Superuser (Idempotent)
echo "Step 4: Checking for Admin User..."
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

# 5. Start Gunicorn
echo "Step 5: Launching Gunicorn..."
exec gunicorn chambalabamba.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120

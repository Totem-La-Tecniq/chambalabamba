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
rsync -av --ignore-existing \
  --exclude='*.css' \
  --exclude='*.js' \
  --exclude='*.map' \
  --exclude='admin/' \
  --exclude='ckeditor/' \
  "$SOURCE" "$DEST"

echo "--- ✅ Media Initialization Complete ---"

# 4. Start Gunicorn
echo "Step 3: Launching Gunicorn..."
exec gunicorn chambalabamba.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
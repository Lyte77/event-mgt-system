import os
import sys
import django
import random
import uuid

from datetime import timedelta
from django.utils.text import slugify
from django.utils import timezone
from faker import Faker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go up one level from 'events/'
sys.path.append(BASE_DIR)

# ---------------------------------------------
# SETUP DJANGO ENVIRONMENT
# ---------------------------------------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')  # <-- change this
django.setup()

from django.contrib.auth import get_user_model
from events.models import Event 

 # <-- adjust app name if different

# ---------------------------------------------
# CONFIG
# ---------------------------------------------
fake = Faker()
User = get_user_model()

# Ensure organizer exists
organizer = User.objects.first()
if not organizer:
    organizer = User.objects.create_user(
        email="organizer@example.com",
        password="password123",
        first_name="John",
        last_name="Doe"
    )

sample_images = [
    "https://images.unsplash.com/photo-1556761175-4b46a572b786",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
    "https://images.unsplash.com/photo-1551836022-d5d88e9218df",
    "https://images.unsplash.com/photo-1531058020387-3be344556be6",
    "https://images.unsplash.com/photo-1521737604893-d14cc237f11d",
    "https://images.unsplash.com/photo-1515168833906-d2a3b82b302a",
    "https://images.unsplash.com/photo-1534447677768-be436bb09401",
    "https://images.unsplash.com/photo-1551836022-4b1b2b1b0e24",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e",
    "https://images.unsplash.com/photo-1503428593586-e225b39bddfe",
]

STATUS_CHOICES = ['upcoming', 'ongoing', 'completed', 'cancelled']

# ---------------------------------------------
# CREATE EVENTS
# ---------------------------------------------
for _ in range(25):
    title = fake.catch_phrase()
    description = fake.paragraph(nb_sentences=6)
    venue = fake.address()
    start_time = timezone.now() + timedelta(days=random.randint(-10, 15))
    end_time = start_time + timedelta(hours=random.randint(2, 8))
    status = random.choice(STATUS_CHOICES)
    capacity = random.randint(50, 500)
    slug = slugify(title) + f"-{uuid.uuid4().hex[:6]}"
    image_url = random.choice(sample_images)

    Event.objects.create(
        organizer=organizer,
        title=title,
        description=description,
        venue=venue,
        start_time=start_time,
        end_time=end_time,
        capacity=capacity,
        status=status,
        slug=slug,
        event_image=image_url,
        is_published=True,
    )

print("✅ Successfully created 25 fake events with Cloudinary images!")

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_store.settings')
django.setup()

from store.models import Category, Medicine
from django.core.files.base import ContentFile

def populate():
    # Create Categories
    pain_relief = Category.objects.create(name='Pain Relief', slug='pain-relief')
    vitamins = Category.objects.create(name='Vitamins & Supplements', slug='vitamins-supplements')
    first_aid = Category.objects.create(name='First Aid', slug='first-aid')

    # Create Medicines
    Medicine.objects.create(
        category=pain_relief,
        name='Paracetamol 500mg',
        slug='paracetamol-500mg',
        description='Effective pain relief for headaches and fever.',
        price=5.99,
        stock=100,
        available=True
    )

    Medicine.objects.create(
        category=pain_relief,
        name='Ibuprofen 200mg',
        slug='ibuprofen-200mg',
        description='Anti-inflammatory pain relief.',
        price=6.50,
        stock=80,
        available=True
    )

    Medicine.objects.create(
        category=vitamins,
        name='Vitamin C 1000mg',
        slug='vitamin-c-1000mg',
        description='Boost your immune system.',
        price=12.00,
        stock=50,
        available=True
    )

    Medicine.objects.create(
        category=first_aid,
        name='Band-Aid Pack',
        slug='band-aid-pack',
        description='Assorted sizes for minor cuts and scrapes.',
        price=3.99,
        stock=200,
        available=True
    )

    print("Database populated successfully.")

if __name__ == '__main__':
    populate()

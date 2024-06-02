from django.core.management.base import BaseCommand
from cryptography.fernet import Fernet


class Command(BaseCommand):
    help = 'Generate crypto key'

    def handle(self, *args, **options):
        print("Do not share this key with anyone!")
        print(f"Key: {Fernet.generate_key().decode()}")

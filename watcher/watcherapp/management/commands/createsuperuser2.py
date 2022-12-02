from django.contrib.auth import get_user_model
from django.core.management import CommandError
from django.core.management.base import BaseCommand
 
 
class Command(BaseCommand):
    help = "Create a superuser or pass"
 
    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            dest="username",
            default=None,
            help="Superuser's username",
        )
        parser.add_argument(
            "--email",
            dest="email",
            default=None,
            help="Superuser's email",
        )
        parser.add_argument(
            "--password",
            dest="password",
            default=None,
            help="Superuser's password",
        )
 
    def handle(self, *args, **options):
        username = options.get("username")
        email = options.get("email")
        password = options.get("password")
 
        if not username or not email or not password:
            raise CommandError("All three arguments --username, --email and --password are required")
 
        User = get_user_model()

        if User.objects.filter(username=username).exists():
            self.stdout.write("Superuser already exists, pass...")
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
from django.core.management.base import BaseCommand
from users.models import User

seed_text = "superuser"


class Command(BaseCommand):

    help = f"This command creates {seed_text}"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:
            User.objects.create_superuser(
                "sgadmin@naver.com", "shoon2430@change1940!!", "ghksxk12"
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))

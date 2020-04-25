import os
from django.core.management.base import BaseCommand
from users.models import User

seed_text = "superuser"


class Command(BaseCommand):
    """
    aws 배포시 superuser생성 커멘드
    """

    help = f"This command creates {seed_text}"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username=os.environ.get("SUPER_ID"))
        if not admin:
            User.objects.create_superuser(
                os.environ.get("SUPER_ID"),
                os.environ.get("SUPER_EMAIL"),
                os.environ.get("SUPER_PASSWORD"),
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))

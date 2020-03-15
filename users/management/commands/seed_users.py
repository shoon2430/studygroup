from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

seed_text = "Users"


class Command(BaseCommand):

    help = f"This command creates {seed_text}"

    def add_arguments(self, parser):

        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {seed_text} you want to create",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(User, number)
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE {seed_text} count : {number}"))


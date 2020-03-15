import random
from django.core.management.base import BaseCommand
from django_seed import Seed

from plans.models import Plan, Feedback
from users.models import User

seed_text = "Feedbacks"


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

        plans = Plan.objects.all()
        users = User.objects.all()

        seeder.add_entity(
            Feedback,
            number,
            {
                "plan": lambda x: random.choice(plans),
                "user": lambda x: random.choice(users),
                "title": lambda x: seeder.faker.name(),
                "contents_for_plan": lambda x: seeder.faker.text(),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE {seed_text} count : {number}"))


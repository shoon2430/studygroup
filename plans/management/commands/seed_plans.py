import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed

from groups.models import Group
from plans.models import Plan, Feedback
from users.models import User


seed_text = "Plans"


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

        users = User.objects.all()
        groups = Group.objects.all()

        seeder.add_entity(
            Plan,
            number,
            {
                "group": lambda x: random.choice(groups),
                "user": lambda x: random.choice(users),
                "title_for_plan": lambda x: seeder.faker.name(),
                "contents_for_plan": lambda x: seeder.faker.text(),
                "title_for_result": lambda x: seeder.faker.name(),
                "contents_for_result": lambda x: seeder.faker.text(),
                "start_day": lambda x: datetime.now(),
                "end_day": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
                "status": lambda x: random.choice(
                    ["ENROLLMENT", "CONFIRM", "COMPLETE", "SUCCESS"]
                ),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE {seed_text} count : {number}"))


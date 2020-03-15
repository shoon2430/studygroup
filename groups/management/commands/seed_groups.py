import random
from django.db.models import Max
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

from groups.models import Group
from plans.models import Plan, Feedback
from users.models import User

seed_text = "Groups"


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

        # users = User.objects.all()

        seeder.add_entity(
            Group,
            number,
            {
                "category": lambda x: random.choice(["S", "R", "E", "H"]),
                "max_group_count": lambda x: random.randint(1, 8),
                "planning_unit": lambda x: random.choice(["week", "day"]),
            },
        )
        create_user = seeder.execute()
        create_clead = flatten(list(create_user.values()))

        for pk in create_clead:

            group = Group.objects.get(pk=pk)

            random_count = random.randint(1, 9)
            max_id = User.objects.all().aggregate(max_id=Max("id"))["max_id"]

            if random_count > group.max_group_count:
                random_count = group.max_group_count

            add_count = 0
            while add_count != random_count:
                pk = random.randint(1, max_id)
                user = User.objects.filter(pk=pk).first()

                if user:
                    group.user.add(user)
                    add_count += 1

        self.stdout.write(self.style.SUCCESS(f"CREATE {seed_text} count : {number}"))


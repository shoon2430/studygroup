import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed

from groups.models import Group
from plans.models import Plan, Feedback
from users.models import User


seed_text = "Plans"


class Command(BaseCommand):
    """
    테스트 데이터를 생성하는 Django커맨드
    Plan에 대한 가짜 데이터를 생성한다.
    실제 운용전 테스트 해보기 위한 데이터가 필요할때 사용한다.

    파일에 대한 데이터는 생성하지 않는다.
    """
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

        now = datetime.now()
        now_year, now_month, now_day = now.year, now.month, now.day
        deadline = datetime(now_year, now_month, now_day, 0, 0, 0)

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
                "deadline": deadline,
                "status": lambda x: random.choice(
                    ["ENROLLMENT", "CONFIRM", "COMPLETE", "SUCCESS"]
                ),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE {seed_text} count : {number}"))

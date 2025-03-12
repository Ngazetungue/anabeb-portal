import random
from django.core.management.base import BaseCommand
from portal.models import Member  # Replace 'portal' with your actual app name
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populate sample members into the database'

    def handle(self, *args, **options):
        sex_choices = ['male', 'female']
        village_choices = [
            "anabeb", "otjondunda", "ombaikiha", "warmquelle", "khowarib", "omukutu", 
            "otjondumbu", "okaturua", "otjatjondjira"
        ]
        status_choices = ['alive', 'deceased']
        first_names = ['John', 'Emily', 'Michael', 'Jessica', 'Daniel', 'Olivia', 'William', 'Sophia', 'James', 'Ava', 'David', 'Charlotte', 'Daniel', 'Mia', 'Lucas']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Taylor', 'Martinez', 'Jones', 'Davis', 'Miller', 'Garcia', 'Lee', 'Anderson', 'Thomas', 'Hernandez', 'Moore']

        today = date.today()

        for i in range(15):
            # Randomly select a first and last name
            first_name = first_names[i % len(first_names)]
            last_name = last_names[i % len(last_names)]

            # Randomly choose gender
            gender = random.choice(sex_choices)

            # Random identification number (up to 10 digits)
            identification_document = random.randint(1000000000, 9999999999)

            # Random date of birth (between 18 and 80 years ago)
            min_birth_date = today - timedelta(days=365*80)
            max_birth_date = today - timedelta(days=365*18)
            date_of_birth = random_date(min_birth_date, max_birth_date)

            # Random phone number (10 digits)
            cellphone_number = ''.join([random.choice('0123456789') for _ in range(10)])

            # Random village
            village = random.choice(village_choices)

            # Random status (alive or deceased)
            status = random.choice(status_choices)

            # Random date of joining (within the last 10 years)
            date_join = today - timedelta(days=random.randint(1, 3650))

            # Ensure that date_join is before date_deceased if the member is deceased
            date_deceased = None
            if status == 'deceased':
                date_deceased = today - timedelta(days=random.randint(1, 3650))
                # Ensure date_join is before date_deceased
                if date_deceased < date_join:
                    date_join = date_deceased - timedelta(days=random.randint(1, 3650))

            # Create and save the member
            member = Member(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                identification_document=str(identification_document),
                date_of_birth=date_of_birth,
                cellphone_number=cellphone_number,
                village=village,
                date_join=date_join,
                status=status,
                date_deceased=date_deceased
            )
            member.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created member: {first_name} {last_name}'))

# Helper function to generate a random date between two dates
def random_date(start_date, end_date):
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    return start_date + timedelta(days=random_days)
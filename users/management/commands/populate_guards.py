import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from portal.models import Guard 

class Command(BaseCommand):
    help = 'Populate sample guards into the database'

    def handle(self, *args, **options):
        # Guard details
        first_names = ['John', 'Emily', 'Michael', 'Jessica', 'Daniel', 'Olivia', 'William', 'Sophia', 'James', 'David', 'Lily', 'Charlie', 'Nina', 'Mia', 'Ethan']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Taylor', 'Martinez', 'Jones', 'Davis', 'Miller', 'Wilson', 'Moore', 'Anderson', 'Thomas', 'Jackson', 'White']
        villages = ['anabeb', 'otjondunda', 'ombaikiha', 'warmquelle', 'khowarib', 'omukutu', 'otjondumbu', 'okaturua', 'otjatjondjira']
        statuses = ['active', 'inactive']

        # Loop to create 15 guards
        for i in range(15):
            first_name = first_names[i]
            last_name = last_names[i % len(last_names)]  # Use last names cyclically
            gender = random.choice(['male', 'female'])
            village_assigned = random.choice(villages)
            status = random.choice(statuses)

            # Generate random date of birth between 20 and 60 years ago
            years = random.randint(20, 60)
            date_of_birth = timezone.now() - timedelta(days=365 * years)

            # Generate a random phone number
            cellphone_number = f"081{random.randint(1000000, 9999999)}"

            # Generate a random identification document (unique 11 digits)
            identification_document = f"{random.randint(1000000000, 9999999999)}"

            # Generate a random date of employment within the last 5 years
            date_employed = timezone.now() - timedelta(days=random.randint(1, 1825))

            # Create Guard instance
            guard = Guard.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                identification_document=identification_document,
                date_of_birth=date_of_birth,
                cellphone_number=cellphone_number,
                village_assigned=village_assigned,
                date_employed=date_employed,
                status=status
            )
            self.stdout.write(self.style.SUCCESS(f'Created guard: {guard.first_name} {guard.last_name}'))

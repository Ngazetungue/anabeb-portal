import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Populate sample users into the database'

    def handle(self, *args, **options):
        User = get_user_model()
        user_types = ['staff', 'admin']
        first_names = ['John', 'Emily']
        last_names = ['Smith', 'Johnson']
        user_count = {user_type: 0 for user_type in user_types}

        for i in range(8):
            user_type = user_types[i % 2]
            if user_count[user_type] < 2:
                user_count[user_type] += 1
            else:
                user_type = random.choice(list(set(user_types) - {user_type}))

            username = f'{first_names[i].lower()}'
            first_name = first_names[i]
            last_name = last_names[i % len(last_names)]
            sex = random.choice(['male', 'female'])
            user = User.objects.create_user(
                username=username,
                email=f'{username}@gmail.com',
                password='password',
                user_type=user_type,
                first_name=first_name,
                last_name=last_name,
                sex=sex,
            )
            self.stdout.write(self.style.SUCCESS(f'Created {user_type} user: {user.username} ({first_name} {last_name})'))

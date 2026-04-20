import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Tworzy domyślnego superużytkownika dla AG Construction (wymaga DJANGO_ADMIN_PASSWORD)'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.environ.get('DJANGO_ADMIN_USER', 'admin')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD', '')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', 'agconstruction39@gmail.com')

        if not password:
            raise CommandError(
                'Ustaw zmienną środowiskową DJANGO_ADMIN_PASSWORD przed uruchomieniem tej komendy.'
            )

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS(
                f'✓ Superużytkownik "{username}" utworzony pomyślnie.'
            ))
        else:
            self.stdout.write(self.style.WARNING(f'Użytkownik "{username}" już istnieje.'))

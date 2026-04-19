from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Tworzy domyślnego superużytkownika dla AG Construction'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'admin'
        password = 'AGConstruction2025!'
        email = 'admin@agconstruction.pl'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Superużytkownik utworzony:\n'
                f'  Login:    {username}\n'
                f'  Hasło:    {password}\n'
                f'  Email:    {email}\n'
                f'  Panel:    http://127.0.0.1:8000/admin/\n'
            ))
        else:
            self.stdout.write(self.style.WARNING(f'Użytkownik "{username}" już istnieje.'))

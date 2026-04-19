from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='RodzajLokalu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=100, unique=True, verbose_name='Nazwa')),
            ],
            options={
                'verbose_name': 'Rodzaj lokalu',
                'verbose_name_plural': 'Rodzaje lokali',
            },
        ),
        migrations.CreateModel(
            name='Inwestycja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=200, verbose_name='Nazwa inwestycji')),
                ('adres', models.CharField(max_length=300, verbose_name='Adres')),
                ('data_dodania', models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')),
                ('zdjecie', models.ImageField(blank=True, null=True, upload_to='inwestycje/', verbose_name='Zdjęcie główne')),
                ('opis', models.TextField(blank=True, null=True, verbose_name='Opis')),
                ('standard', models.TextField(blank=True, null=True, verbose_name='Standard wykończenia')),
                ('unikalny_identyfikator_przedsiewziecia', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Unikalny identyfikator przedsięwzięcia')),
                ('numer_pozwolenia', models.CharField(blank=True, max_length=100, null=True, verbose_name='Numer pozwolenia na budowę')),
                ('termin_rozpoczecia', models.DateField(blank=True, null=True, verbose_name='Termin rozpoczęcia')),
                ('termin_zakonczenia', models.DateField(blank=True, null=True, verbose_name='Planowany termin zakończenia')),
                ('prospekt_pdf', models.FileField(blank=True, null=True, upload_to='prospekty/', verbose_name='Prospekt informacyjny (PDF)')),
            ],
            options={
                'verbose_name': 'Inwestycja',
                'verbose_name_plural': 'Inwestycje',
                'ordering': ['-data_dodania'],
            },
        ),
        migrations.CreateModel(
            name='InwestycjaZdjecie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obraz', models.ImageField(upload_to='galeria/', verbose_name='Zdjęcie')),
                ('kolejnosc', models.PositiveIntegerField(default=0, verbose_name='Kolejność')),
                ('inwestycja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zdjecia', to='oferty.inwestycja', verbose_name='Inwestycja')),
            ],
            options={
                'verbose_name': 'Zdjęcie inwestycji',
                'verbose_name_plural': 'Zdjęcia inwestycji',
                'ordering': ['kolejnosc'],
            },
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adres', models.CharField(max_length=255, verbose_name='Adres lokalu')),
                ('metraz', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Metraż (m²)')),
                ('pokoje', models.IntegerField(verbose_name='Liczba pokoi')),
                ('status', models.CharField(choices=[('dostepne', 'Dostępne'), ('sprzedane', 'Sprzedane'), ('rezerwacja', 'Rezerwacja'), ('w_budowie', 'W budowie')], default='dostepne', max_length=20, verbose_name='Status')),
                ('data_dodania', models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')),
                ('zdjecie', models.ImageField(blank=True, null=True, upload_to='oferty/', verbose_name='Zdjęcie')),
                ('numer_lokalu', models.CharField(blank=True, max_length=50, null=True, verbose_name='Numer lokalu')),
                ('numer_oferty', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Numer oferty')),
                ('rzut', models.ImageField(blank=True, null=True, upload_to='rzuty/', verbose_name='Rzut lokalu')),
                ('pietro', models.IntegerField(blank=True, null=True, verbose_name='Piętro')),
                ('inwestycja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oferty', to='oferty.inwestycja', verbose_name='Inwestycja')),
                ('rodzaj_lokalu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='oferty.rodzajlokalu', verbose_name='Rodzaj lokalu')),
            ],
            options={
                'verbose_name': 'Oferta',
                'verbose_name_plural': 'Oferty',
                'ordering': ['-data_dodania'],
            },
        ),
        migrations.CreateModel(
            name='Cena',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kwota', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Kwota (PLN)')),
                ('data', models.DateField(verbose_name='Data')),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ceny', to='oferty.oferta', verbose_name='Oferta')),
            ],
            options={
                'verbose_name': 'Cena',
                'verbose_name_plural': 'Ceny',
                'ordering': ['data'],
            },
        ),
        migrations.CreateModel(
            name='PomieszczeniePrzynalezne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=200, verbose_name='Nazwa')),
                ('powierzchnia', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Powierzchnia (m²)')),
                ('cena', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Cena (PLN)')),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pomieszczenia', to='oferty.oferta', verbose_name='Oferta')),
            ],
            options={
                'verbose_name': 'Pomieszczenie przynależne',
                'verbose_name_plural': 'Pomieszczenia przynależne',
            },
        ),
        migrations.CreateModel(
            name='SwiadczeniePieniezne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=200, verbose_name='Nazwa')),
                ('kwota', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Kwota (PLN)')),
                ('opis', models.TextField(blank=True, null=True, verbose_name='Opis')),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swiadczenia', to='oferty.oferta', verbose_name='Oferta')),
            ],
            options={
                'verbose_name': 'Świadczenie pieniężne',
                'verbose_name_plural': 'Świadczenia pieniężne',
            },
        ),
        migrations.CreateModel(
            name='Rabat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=200, verbose_name='Nazwa')),
                ('wartosc', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Wartość')),
                ('typ', models.CharField(choices=[('procentowy', 'Procentowy'), ('kwotowy', 'Kwotowy')], max_length=20, verbose_name='Typ rabatu')),
                ('data_od', models.DateField(verbose_name='Data od')),
                ('data_do', models.DateField(verbose_name='Data do')),
                ('oferta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rabaty', to='oferty.oferta', verbose_name='Oferta')),
            ],
            options={
                'verbose_name': 'Rabat',
                'verbose_name_plural': 'Rabaty',
            },
        ),
    ]

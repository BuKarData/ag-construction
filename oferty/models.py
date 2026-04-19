from django.db import models


class RodzajLokalu(models.Model):
    nazwa = models.CharField(max_length=100, unique=True, verbose_name='Nazwa')

    class Meta:
        verbose_name = 'Rodzaj lokalu'
        verbose_name_plural = 'Rodzaje lokali'

    def __str__(self):
        return self.nazwa


class Inwestycja(models.Model):
    nazwa = models.CharField(max_length=200, verbose_name='Nazwa inwestycji')
    adres = models.CharField(max_length=300, verbose_name='Adres')
    data_dodania = models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')
    zdjecie = models.ImageField(upload_to='inwestycje/', blank=True, null=True, verbose_name='Zdjęcie główne')
    opis = models.TextField(blank=True, null=True, verbose_name='Opis')
    standard = models.TextField(blank=True, null=True, verbose_name='Standard wykończenia')
    unikalny_identyfikator_przedsiewziecia = models.CharField(
        max_length=100, unique=True, blank=True, null=True,
        verbose_name='Unikalny identyfikator przedsięwzięcia'
    )
    numer_pozwolenia = models.CharField(max_length=100, blank=True, null=True, verbose_name='Numer pozwolenia na budowę')
    termin_rozpoczecia = models.DateField(blank=True, null=True, verbose_name='Termin rozpoczęcia')
    termin_zakonczenia = models.DateField(blank=True, null=True, verbose_name='Planowany termin zakończenia')
    prospekt_pdf = models.FileField(upload_to='prospekty/', blank=True, null=True, verbose_name='Prospekt informacyjny (PDF)')

    class Meta:
        verbose_name = 'Inwestycja'
        verbose_name_plural = 'Inwestycje'
        ordering = ['-data_dodania']

    def __str__(self):
        return self.nazwa


class InwestycjaZdjecie(models.Model):
    inwestycja = models.ForeignKey(Inwestycja, on_delete=models.CASCADE, related_name='zdjecia', verbose_name='Inwestycja')
    obraz = models.ImageField(upload_to='galeria/', verbose_name='Zdjęcie')
    kolejnosc = models.PositiveIntegerField(default=0, verbose_name='Kolejność')

    class Meta:
        verbose_name = 'Zdjęcie inwestycji'
        verbose_name_plural = 'Zdjęcia inwestycji'
        ordering = ['kolejnosc']

    def __str__(self):
        if self.inwestycja and self.inwestycja.nazwa:
            return f'Zdjęcie – {self.inwestycja.nazwa}'
        return 'Zdjęcie inwestycji'


class Oferta(models.Model):
    STATUS_CHOICES = [
        ('dostepne', 'Dostępne'),
        ('sprzedane', 'Sprzedane'),
        ('rezerwacja', 'Rezerwacja'),
        ('w_budowie', 'W budowie'),
    ]

    inwestycja = models.ForeignKey(Inwestycja, on_delete=models.CASCADE, related_name='oferty', verbose_name='Inwestycja')
    adres = models.CharField(max_length=255, verbose_name='Adres lokalu')
    metraz = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Metraż (m²)')
    pokoje = models.IntegerField(verbose_name='Liczba pokoi')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dostepne', verbose_name='Status')
    data_dodania = models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')
    zdjecie = models.ImageField(upload_to='oferty/', blank=True, null=True, verbose_name='Zdjęcie')
    numer_lokalu = models.CharField(max_length=50, blank=True, null=True, verbose_name='Numer lokalu')
    numer_oferty = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name='Numer oferty')
    rodzaj_lokalu = models.ForeignKey(
        RodzajLokalu, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Rodzaj lokalu'
    )
    rzut = models.ImageField(upload_to='rzuty/', blank=True, null=True, verbose_name='Rzut lokalu')
    pietro = models.IntegerField(blank=True, null=True, verbose_name='Piętro')

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Oferty'
        ordering = ['-data_dodania']

    def __str__(self):
        return f'{self.numer_lokalu or self.adres} – {self.inwestycja}'

    def aktualna_cena(self):
        cena = self.ceny.order_by('-data').first()
        return cena.kwota if cena else None

    def cena_za_m2(self):
        cena = self.aktualna_cena()
        if cena and self.metraz:
            return round(cena / self.metraz, 2)
        return None


class Cena(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='ceny', verbose_name='Oferta')
    kwota = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Kwota (PLN)')
    data = models.DateField(verbose_name='Data')

    class Meta:
        verbose_name = 'Cena'
        verbose_name_plural = 'Ceny'
        ordering = ['data']

    def __str__(self):
        return f'{self.oferta} – {self.kwota} PLN ({self.data})'


class PomieszczeniePrzynalezne(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='pomieszczenia', verbose_name='Oferta')
    nazwa = models.CharField(max_length=200, verbose_name='Nazwa')
    powierzchnia = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Powierzchnia (m²)')
    cena = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Cena (PLN)')

    class Meta:
        verbose_name = 'Pomieszczenie przynależne'
        verbose_name_plural = 'Pomieszczenia przynależne'

    def __str__(self):
        return f'{self.nazwa} – {self.oferta}'


class SwiadczeniePieniezne(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='swiadczenia', verbose_name='Oferta')
    nazwa = models.CharField(max_length=200, verbose_name='Nazwa')
    kwota = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Kwota (PLN)')
    opis = models.TextField(blank=True, null=True, verbose_name='Opis')

    class Meta:
        verbose_name = 'Świadczenie pieniężne'
        verbose_name_plural = 'Świadczenia pieniężne'

    def __str__(self):
        return f'{self.nazwa} – {self.kwota} PLN'


class Rabat(models.Model):
    TYP_CHOICES = [
        ('procentowy', 'Procentowy'),
        ('kwotowy', 'Kwotowy'),
    ]

    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='rabaty', verbose_name='Oferta')
    nazwa = models.CharField(max_length=200, verbose_name='Nazwa')
    wartosc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Wartość')
    typ = models.CharField(max_length=20, choices=TYP_CHOICES, verbose_name='Typ rabatu')
    data_od = models.DateField(verbose_name='Data od')
    data_do = models.DateField(verbose_name='Data do')

    class Meta:
        verbose_name = 'Rabat'
        verbose_name_plural = 'Rabaty'

    def __str__(self):
        return f'{self.nazwa} – {self.oferta}'

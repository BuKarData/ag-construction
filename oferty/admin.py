from django.contrib import admin
from .models import (
    Inwestycja, InwestycjaZdjecie, Oferta, Cena,
    RodzajLokalu, PomieszczeniePrzynalezne, SwiadczeniePieniezne, Rabat
)


@admin.register(RodzajLokalu)
class RodzajLokaluAdmin(admin.ModelAdmin):
    list_display = ['nazwa']
    search_fields = ['nazwa']


class InwestycjaZdjecieInline(admin.TabularInline):
    model = InwestycjaZdjecie
    extra = 1
    fields = ['obraz', 'kolejnosc']


@admin.register(Inwestycja)
class InwestycjaAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'adres', 'termin_zakonczenia', 'data_dodania']
    search_fields = ['nazwa', 'adres']
    list_filter = ['termin_zakonczenia']
    inlines = [InwestycjaZdjecieInline]
    fieldsets = [
        ('Podstawowe informacje', {
            'fields': ['nazwa', 'adres', 'zdjecie', 'opis', 'standard']
        }),
        ('Dane formalne', {
            'fields': [
                'unikalny_identyfikator_przedsiewziecia',
                'numer_pozwolenia',
                'termin_rozpoczecia',
                'termin_zakonczenia',
                'prospekt_pdf',
            ]
        }),
    ]


class CenaInline(admin.TabularInline):
    model = Cena
    extra = 1
    fields = ['kwota', 'data']


class PomieszczeniaInline(admin.TabularInline):
    model = PomieszczeniePrzynalezne
    extra = 1


class SwiadczeniaInline(admin.TabularInline):
    model = SwiadczeniePieniezne
    extra = 0


class RabatyInline(admin.TabularInline):
    model = Rabat
    extra = 0


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ['numer_lokalu', 'inwestycja', 'adres', 'metraz', 'ogrodek_metraz', 'pokoje', 'status', 'aktualna_cena']
    list_filter = ['status', 'inwestycja', 'rodzaj_lokalu']
    search_fields = ['numer_lokalu', 'numer_oferty', 'adres']
    inlines = [CenaInline, PomieszczeniaInline, SwiadczeniaInline, RabatyInline]
    readonly_fields = ['data_dodania']

    @admin.display(description='Aktualna cena')
    def aktualna_cena(self, obj):
        cena = obj.aktualna_cena()
        if cena:
            return f'{cena:,.0f} PLN'.replace(',', ' ')
        return '—'


@admin.register(Cena)
class CenaAdmin(admin.ModelAdmin):
    list_display = ['oferta', 'kwota', 'data']
    list_filter = ['data']

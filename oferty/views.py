import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Inwestycja, Oferta, Cena
from .forms import OfertaForm, CenaForm


def safe_float(value):
    try:
        if value is None:
            return None
        return float(str(value).replace(',', '.').replace(' ', ''))
    except (ValueError, TypeError):
        return None


def home(request):
    inwestycje = Inwestycja.objects.prefetch_related(
        'oferty__ceny', 'zdjecia'
    ).all()

    for inv in inwestycje:
        for oferta in inv.oferty.all():
            ceny = list(oferta.ceny.all())
            oferta._aktualna_cena = ceny[-1].kwota if ceny else None
            metraz = safe_float(oferta.metraz)
            cena = safe_float(oferta._aktualna_cena)
            oferta._cena_m2 = round(cena / metraz, 0) if cena and metraz else None

    return render(request, 'home.html', {'inwestycje': inwestycje})


def lista_ofert(request):
    oferty = Oferta.objects.select_related('inwestycja', 'rodzaj_lokalu').prefetch_related('ceny').order_by('-data_dodania')

    oferty_data = []
    for oferta in oferty:
        ceny = list(oferta.ceny.all())
        aktualna = ceny[-1].kwota if ceny else None
        metraz = safe_float(oferta.metraz)
        cena_val = safe_float(aktualna)
        cena_m2 = round(cena_val / metraz, 0) if cena_val and metraz else None

        historia = [
            {'data': str(c.data), 'kwota': safe_float(c.kwota)}
            for c in ceny
        ]

        oferty_data.append({
            'obj': oferta,
            'aktualna_cena': aktualna,
            'cena_m2': cena_m2,
            'historia_json': json.dumps(historia, ensure_ascii=False),
        })

    return render(request, 'oferty/lista_ofert.html', {'oferty_data': oferty_data})


def szczegoly_inwestycji(request, pk):
    inwestycja = get_object_or_404(Inwestycja, pk=pk)
    return render(request, 'oferty/szczegoly_inwestycji.html', {'inwestycja': inwestycja})


def dodaj_oferte(request):
    if request.method == 'POST':
        form = OfertaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ofert')
    else:
        form = OfertaForm()
    return render(request, 'oferty/dodaj_oferte.html', {'form': form})


def dodaj_cene(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    if request.method == 'POST':
        form = CenaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ofert')
    else:
        form = CenaForm(initial={'oferta': oferta})
    return render(request, 'oferty/dodaj_cene.html', {'form': form, 'oferta': oferta})


@csrf_exempt
def ajax_dodaj_cene(request, oferta_id):
    if request.method == 'POST':
        oferta = get_object_or_404(Oferta, pk=oferta_id)
        try:
            kwota = request.POST.get('kwota')
            data = request.POST.get('data')
            Cena.objects.create(oferta=oferta, kwota=Decimal(kwota), data=data)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Metoda niedozwolona'})

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('oferty/', views.lista_ofert, name='lista_ofert'),
    path('inwestycje/<int:pk>/', views.szczegoly_inwestycji, name='szczegoly_inwestycji'),
    path('oferty/dodaj/', views.dodaj_oferte, name='dodaj_oferte'),
    path('oferty/<int:oferta_id>/cena/', views.dodaj_cene, name='dodaj_cene'),
    path('oferty/<int:oferta_id>/cena/ajax/', views.ajax_dodaj_cene, name='ajax_dodaj_cene'),
]

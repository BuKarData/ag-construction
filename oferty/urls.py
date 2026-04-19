from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.home, name='home'),
    path('oferty/', views.lista_ofert, name='lista_ofert'),
    path('inwestycje/<int:pk>/', views.szczegoly_inwestycji, name='szczegoly_inwestycji'),
    path('oferta/<int:pk>/', views.szczegoly_oferty, name='szczegoly_oferty'),
    path('oferty/dodaj/', views.dodaj_oferte, name='dodaj_oferte'),
    path('oferty/<int:oferta_id>/cena/', views.dodaj_cene, name='dodaj_cene'),
    path('oferty/<int:oferta_id>/cena/ajax/', views.ajax_dodaj_cene, name='ajax_dodaj_cene'),
    # Open Data API
    path('api/data.csv', api.view_csv, name='api-csv'),
    path('api/data.xlsx', api.view_xlsx, name='api-xlsx'),
    path('api/data.jsonld', api.view_jsonld, name='api-jsonld'),
    path('api/metadata.xml', api.view_metadata_xml, name='api-metadata'),
    path('api/data.csv.md5', api.view_md5, {'fmt': 'csv'}, name='api-csv-md5'),
    path('api/data.xlsx.md5', api.view_md5, {'fmt': 'xlsx'}, name='api-xlsx-md5'),
    path('api/data.jsonld.md5', api.view_md5, {'fmt': 'jsonld'}, name='api-jsonld-md5'),
    path('api/metadata.xml.md5', api.view_md5, {'fmt': 'xml'}, name='api-xml-md5'),
]

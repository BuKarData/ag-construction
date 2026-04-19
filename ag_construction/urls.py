from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'AG Construction – Panel Administracyjny'
admin.site.site_title = 'AG Construction'
admin.site.index_title = 'Zarządzanie ofertami'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('oferty.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

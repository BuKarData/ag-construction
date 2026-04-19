from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

admin.site.site_header = 'AG Construction – Panel Administracyjny'
admin.site.site_title = 'AG Construction'
admin.site.index_title = 'Zarządzanie ofertami'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('oferty.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

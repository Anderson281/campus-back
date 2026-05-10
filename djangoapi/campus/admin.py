from django.contrib import admin

# Register your models here.
# Registra los modelos para poder revisarlos desde el panel de administracion de Django.

from campus.models import Punto, Linea, Poligono

admin.site.register(Punto)
admin.site.register(Linea)
admin.site.register(Poligono)

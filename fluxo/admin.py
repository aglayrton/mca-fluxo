from django.contrib import admin
from fluxo.models import FluxoAgua

class FluxoAguas(admin.ModelAdmin):
    list_display = ('id', 'consumo_diario', 'data')
    list_display_links = ('id', 'consumo_diario',)
    list_per_page = 7
    search_fields = ('data',)

admin.site.register(FluxoAgua, FluxoAguas)


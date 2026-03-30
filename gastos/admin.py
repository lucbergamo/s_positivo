from django.contrib import admin
from .models import Gasto

'''
@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "classificacao", "data_gasto", "valor", "criado_em")
    list_filter = ("classificacao", "data_gasto", "criado_em")
    search_fields = ("nome", )
    ordering = ("-data_gasto", "-criado_em")'''
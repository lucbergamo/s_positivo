from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, gastos_var, excluir_gasto


urlpatterns = [
    path('', index, name='index'),
    path('gastos/', gastos_var, name='gastos_var'),
    path('excluir_gasto/<int:id>/', excluir_gasto, name='excluir_gasto'),
]
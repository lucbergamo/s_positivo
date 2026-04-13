from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, gastos_var, excluir_gasto, login, logout, gastos_fixos, novo_gasto_fixo, editar_gasto_fixo


urlpatterns = [
    path('', index, name='index'),
    path('gastos/', gastos_var, name='gastos_var'),
    path('excluir_gasto/<int:pk>/', excluir_gasto, name='excluir_gasto'),
    path('login/', login, name='login'),
    path('logout', logout, name='logout'),
    path('gastos_fixos', gastos_fixos, name='gastos_fixos'),
    path('novo_gasto_fixo', novo_gasto_fixo, name='novo_gasto_fixo'),
    path('gastos_fixos/<int:pk>/editar', editar_gasto_fixo, name='editar_gastos_fixos'),
]
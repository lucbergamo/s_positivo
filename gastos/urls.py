from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, gastos_var, excluir_gasto, login, logout, gastos_fixos, novo_gasto_fixo, editar_gasto_fixo, excluir_gasto_fixo, gerar_compromissos, reg_gastos_fixos, reg_compromissos


urlpatterns = [
    path('', index, name='index'),
    path('gastos/', gastos_var, name='gastos_var'),
    path('excluir_gasto/<int:pk>/', excluir_gasto, name='excluir_gasto'),
    path('login/', login, name='login'),
    path('logout', logout, name='logout'),
    path('gastos_fixos', gastos_fixos, name='gastos_fixos'),
    path('novo_gasto_fixo', novo_gasto_fixo, name='novo_gasto_fixo'),
    path('gastos_fixos/<int:pk>/editar', editar_gasto_fixo, name='editar_gastos_fixos'),
    path('excluir_gasto_fixo/<int:pk>/', excluir_gasto_fixo, name='excluir_gasto_fixo'),
    path('gerar_compromissos/', gerar_compromissos, name='gerar_compromissos'),
    path('reg_gastos_fixos/', reg_gastos_fixos, name='reg_gastos_fixos'),
    path('reg_compromissos/<int:pk>', reg_compromissos, name='reg_compromissos'),
]
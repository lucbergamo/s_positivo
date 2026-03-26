from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, gastos


urlpatterns = [
    path('', index, name='index'),
    path('gastos/', gastos, name='gastos'),
]
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Gasto
from django.utils import timezone
from .forms import GastoForm

def filtroMesAtual():
    hoje = timezone.localdate()
    inicio_mes = hoje.replace(day=1)
    
    if inicio_mes.month == 12:
        inicio_prox_mes = inicio_mes.replace(year=inicio_mes.year + 1, month=1)
    else:
        inicio_prox_mes = inicio_mes.replace(month=inicio_mes.month + 1)
    return inicio_mes, inicio_prox_mes
    #return {"inicio_mes": inicio_mes, "inicio_prox_mes": inicio_prox_mes}


def index(request):
    return render(request, 'index.html')
    
def gastos_var(request):
    inicio_mes, inicio_prox_mes = filtroMesAtual()
    dados = Gasto.objects.filter(data_gasto__gte=inicio_mes, data_gasto__lt=inicio_prox_mes).order_by('data_gasto')
    if request.method == "POST":
            form = GastoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Registro criado com sucesso!")
                return redirect("gastos_var")
    else:
            form = GastoForm()
    return render(request, 'gastos_var.html', {"form": form, "itens": dados})

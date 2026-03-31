from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
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


def total_compras_mes_atual():
    hoje = timezone.now()
    
    # Filtra as compras pelo ano e mês atuais
    resultado = Gasto.objects.filter(
        data_gasto__year=hoje.year,
        data_gasto__month=hoje.month
    ).aggregate(total=Sum('valor')) 
    
    # O aggregate retorna um dicionário: {'total': Decimal('0.00')}
    # Usamos 'or 0' para evitar erro caso não haja compras no mês
    return resultado['total'] or 0

def index(request):
    soma = total_compras_mes_atual()
    return render(request, 'index.html', {"soma": round( soma,2)})
    
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

def excluir_gasto(request, id):
    gasto = get_object_or_404(Gasto,id=id)
    if request.method == "POST": # Por segurança, sempre use POST para deletar
        gasto.delete()
        return redirect('gasto_var')

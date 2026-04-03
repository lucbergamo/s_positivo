from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.db.models import Sum
from .models import Gasto
from django.utils import timezone
from .forms import GastoForm, LoginForms

def filtroMesAtual():
    hoje = timezone.localdate()
    inicio_mes = hoje.replace(day=1)
    
    if inicio_mes.month == 12:
        inicio_prox_mes = inicio_mes.replace(year=inicio_mes.year + 1, month=1)
    else:
        inicio_prox_mes = inicio_mes.replace(month=inicio_mes.month + 1)
    return inicio_mes, inicio_prox_mes
    #return {"inicio_mes": inicio_mes, "inicio_prox_mes": inicio_prox_mes}

def login(request):
        form = LoginForms()

        if request.method == "POST":
                form = LoginForms(request.POST)
                
                if form.is_valid():
                        nome=form['nome_login'].value()
                        senha=form['senha'].value()

                usuario = auth.authenticate(
                        username=nome,
                        password=senha
                )

                if usuario is not None:
                        auth.login(request, usuario)
                        messages.success(request, f"{nome} logado com sucesso!")
                        return redirect('index')
                else:
                        messages.error(request, "Usuário ou senha incorreto")
                        return redirect('login')

        return render(request,'login.html',{"form": form})

def logout(request):
        auth.logout(request)
        return redirect('login')

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
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    soma = total_compras_mes_atual()
    return render(request,'index.html', {"soma": round( soma,2)})

    
def gastos_var(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
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

def excluir_gasto(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    form = GastoForm
    inicio_mes, inicio_prox_mes = filtroMesAtual()
    dados = Gasto.objects.filter(data_gasto__gte=inicio_mes, data_gasto__lt=inicio_prox_mes).order_by('data_gasto')
    gastoExcluir = get_object_or_404(Gasto,id=pk)
    if request.method == "POST": # Por segurança, sempre use POST para deletar
        gastoExcluir.delete()
        messages.success(request, "Registro excluído com sucesso!")
        return redirect('gastos_var')
    return render(request, 'gastos_var.html', {"form": form, "itens": dados})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from datetime import date
from decimal import Decimal
from django.db.models import Sum
from .models import Gasto, Gasto_Fixo, Compromissos
from django.utils import timezone
from .forms import GastoForm, LoginForms, GastoFixoForm, CompromissoForm

# ========== Funções de Data ===============
def filtroMesAtual():
    hoje = timezone.localdate()
    inicio_mes = hoje.replace(day=1)
    
    if inicio_mes.month == 12:
        inicio_prox_mes = inicio_mes.replace(year=inicio_mes.year + 1, month=1)
    else:
        inicio_prox_mes = inicio_mes.replace(month=inicio_mes.month + 1)
    return inicio_mes, inicio_prox_mes
    #return {"inicio_mes": inicio_mes, "inicio_prox_mes": inicio_prox_mes}

def nomeMesAtual():
    mes = timezone.now().month
    ano = timezone.now().year
    match mes:
         case 1:
              return "Janeiro - " + str(ano)
         case 2:
                return "Fevereiro - " + str(ano)
         case 3:
            return "Março - " + str(ano)
         case 4:
            return "Abril - " + str(ano)
         case 5:
               return "Maio - " + str(ano)
         case 6:
            return "Junho - " + str(ano)
         case 7:
            return "Julho - " + str(ano)
         case 8:
            return "Agosto - " + str(ano)
         case 9:
            return "Setembro - " + str(ano)
         case 10:
            return "Outubro - " + str(ano)
         case 11:
              return "Novembro - " + str(ano)
         case 12:
              return "Dezembro - " + str(ano)


# ========== Funções de Login ===============
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
                        return redirect('index')
                else:
                        messages.error(request, "Usuário ou senha incorreto")
                        return redirect('login')

        return render(request,'login.html',{"form": form})

def logout(request):
        auth.logout(request)
        return redirect('login')


# ========== Funções de Relatório ===============
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


# ========== Funções de Navegação ===============
def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    soma = total_compras_mes_atual()
    nome_usuario = request.user.get_full_name()
    return render(request,'index.html', {"soma": round( soma,2), "nome": nome_usuario})

@login_required   
def gastos_var(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    mesatual = nomeMesAtual()
    nome_usuario = request.user.get_full_name()
    inicio_mes, inicio_prox_mes = filtroMesAtual()
    dados = Gasto.objects.filter(data_gasto__gte=inicio_mes, data_gasto__lt=inicio_prox_mes).order_by('data_gasto')

    if request.method == "POST":
            form = GastoForm(request.POST)
            if form.is_valid():
                gasto = form.save(commit=False)
                gasto.criado_por = request.user #incluir campo criado_por do usuário conectado
                gasto.save()
                messages.success(request, "Registro criado com sucesso!")
                return redirect("gastos_var")
    else:
        form = GastoForm()
    return render(request, 'gastos_var.html', {"form": form, "itens": dados, "mesatual": mesatual, "nome": nome_usuario})


@login_required   
def gastos_fixos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    mesatual = nomeMesAtual()
    nome_usuario = request.user.get_full_name()
    dados = Gasto_Fixo.objects.all()
    return render(request, 'gastos_fixos.html', { "nome": nome_usuario, "itens": dados})

@login_required   
def novo_gasto_fixo(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    nome_usuario = request.user.get_full_name()
    if request.method == "POST":
            form = GastoFixoForm(request.POST)
            if form.is_valid():
                gasto = form.save(commit=False)
                gasto.criado_por = request.user #incluir campo criado_por do usuário conectado
                gasto.save()
                messages.success(request, "Gasto Fixo criado com sucesso!")
                return redirect("gastos_fixos")
    else:
        form = GastoFixoForm()
    return render(request, 'novo_gasto_fixo.html', {"form": form, "nome": nome_usuario})


@login_required
def editar_gasto_fixo(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    nome_usuario = request.user.get_full_name()

    gasto = get_object_or_404(Gasto_Fixo, pk=pk)

    if request.method == "POST":
        form = GastoFixoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()  # atualiza o mesmo registro
            messages.success(request, "Gasto Fixo atualizado com sucesso!")
            return redirect("gastos_fixos")
    else:
        form = GastoFixoForm(instance=gasto)  # <-- pré-preenche

    return render(request, "novo_gasto_fixo.html", {
        "form": form,
        "nome": nome_usuario,
        "editando": True,
        "gasto": gasto,
    })


# ========== Funções de Exclusão ===============
def excluir_gasto_fixo(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    form = GastoFixoForm
    dados = Gasto_Fixo.objects.all().order_by('data_compensacao')
    gastoExcluir = get_object_or_404(Gasto_Fixo,id=pk)
    if request.method == "POST": # Por segurança, sempre use POST para deletar
        gastoExcluir.delete()
        messages.success(request, "Registro excluído com sucesso!")
        return redirect('gastos_fixos')
    return render(request, 'gastos_fixos.html', {"form": form, "itens": dados})

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

# ========== Gerar compromissos ===============
def gerar_compromissos(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    gastosFixos = Gasto_Fixo.objects.all()
    hoje = timezone.localdate()

    for gasto in gastosFixos:

        obj = Compromissos.objects.create(
                nome= gasto.nome,
                data_compromisso=date(hoje.year, hoje.month, gasto.data_compensacao),
                valor_provisonado=Decimal(gasto.valor_provisonado),
                # classificacao=...  # se for obrigatório
        )
    #Compromissos.objects.all().delete()
    return redirect("gastos_fixos")
    


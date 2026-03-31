from django.shortcuts import render, redirect
from .models import Gasto
from .forms import GastoForm

def index(request):
    return render(request, 'index.html')
    
def gastos_var(request):
    dados = Gasto.objects.all().order_by('data_gasto')[:10]
    if request.method == "POST":
            form = GastoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("gastos_var")
    else:
            form = GastoForm()
    return render(request, 'gastos_var.html', {"form": form, "itens": dados})

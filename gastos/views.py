from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
    
def gastos(request):
    return render(request, 'gastos_variaveis.html')
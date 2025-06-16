from django.shortcuts import render

def acesso_negado(request):
    return render(request, 'acesso_negado.html')
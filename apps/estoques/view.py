from django.shortcuts import render


def menus(request):
    user = request.user
    return render(request, 'estoque/menus.html')
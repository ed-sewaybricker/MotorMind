from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

def index(request: HttpRequest):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        matricula = request.POST.get('matricula', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, matricula=matricula, password=password)

        if user is not None:
            login(request, user)

            if user.senha_temporaria:
                return redirect('alterar_senha_obrigatoria')
            
            return redirect('dashboard')

        return render(request, 'login.html', {
            'erro': 'Matrícula ou senha inválidas'
        })

    return render(request, 'login.html')


@login_required
def alterar_senha_obrigatoria(request: HttpRequest):
    if request.method == 'POST':
        nova_senha = request.POST.get('senha')

        if nova_senha:
            user = request.user
            user.set_password(nova_senha)
            user.senha_temporaria = False
            user.save()

            login(request, user)

            return redirect('dashboard')

    return render(request, 'alterar_senha.html')


@login_required
def sair(request: HttpRequest):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return redirect('dashboard')
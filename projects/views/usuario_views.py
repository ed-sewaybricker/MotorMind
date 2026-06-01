from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, Http404, HttpResponseForbidden

from ..models import Usuarios
from ..permissions import is_admin, is_staff_or_admin

@login_required
def usuarios(request: HttpRequest):
    
    if not is_staff_or_admin(request.user):
        raise Http404()

    usuarios = Usuarios.objects.all().order_by('id_usuario')

    return render(request, 'usuarios.html', {
        'usuarios': usuarios
    })

@login_required
def novo_usuario(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()

    if request.method == 'POST':

        matricula = (request.POST.get('matricula') or '').strip()
        nome = (request.POST.get('nome') or '').strip()
        senha = (request.POST.get('senha') or '').strip()

        if not all([matricula, nome, senha]):
            return redirect('administrador')
        
        usuario_existente = Usuarios.objects.filter(matricula=matricula).exists()

        if usuario_existente:
            return redirect('administrador')

        usuario = Usuarios.objects.create_user(matricula=str(matricula), password=str(senha), nome=str(nome))

        add_as_admin = request.POST.get('is_admin')

        if is_admin(request.user):
            if add_as_admin:
                usuario.nivel_acesso = "ADMIN"
                usuario.is_staff = True
                usuario.is_superuser = True
            else:
                usuario.nivel_acesso = "USER"
                usuario.is_staff = False
                usuario.is_superuser = False
        else:
            usuario.nivel_acesso = "USER"
            usuario.is_staff = False
            usuario.is_superuser = False

        usuario.senha_temporaria = True
        usuario.save()

        return redirect('administrador')

    return redirect('administrador')

@login_required
def editar_usuario(request: HttpRequest, id_usuario: int):

    if not is_staff_or_admin(request.user):
        raise Http404()

    usuario = get_object_or_404(Usuarios, id_usuario=id_usuario)

    if request.user.nivel_acesso == "STAFF" and usuario.nivel_acesso in ["ADMIN", "STAFF"]:
        return HttpResponseForbidden("Sem permissão.")

    if request.method == 'POST':
        usuario.nome = request.POST.get('nome', '').strip()

        if is_admin(request.user):
            nivel = request.POST.get('nivel_acesso')
            if nivel in ["ADMIN", "STAFF", "USER"]:
                usuario.nivel_acesso = nivel

        usuario.save()
        return redirect('administrador')

    return render(request, 'usuarios/editar_usuario.html', {
        'usuario': usuario
    })

@login_required
def deletar_usuario(request: HttpRequest, id_usuario: int):

    if not is_staff_or_admin(request.user):
        raise Http404()

    usuario = get_object_or_404(Usuarios, id_usuario=id_usuario)

    if request.user.nivel_acesso == "STAFF" and usuario.nivel_acesso in ["ADMIN", "STAFF"]:
        return HttpResponseForbidden("Sem permissão.")

    if request.method == 'POST':
        usuario.delete()
        return redirect('administrador')

    return render(request, 'usuarios/confirmar_delete.html', {
        'usuario': usuario
    })

@login_required
def reset(request: HttpRequest, id_usuario: int):

    if not is_staff_or_admin(request.user):
        raise Http404()

    usuario = get_object_or_404(Usuarios, id_usuario=id_usuario)

    if request.user.nivel_acesso == "STAFF" and usuario.nivel_acesso != "USER":
        return HttpResponseForbidden("Sem permissão.")

    if request.method == 'POST':
        nova_senha = request.POST.get('senha', '').strip()

        if nova_senha:
            usuario.set_password(nova_senha)
            usuario.senha_temporaria = True
            usuario.save()

        return redirect('administrador')

    return render(request, 'usuarios/reset_senha.html', {
        'usuario': usuario
    })

@login_required
def promover(request: HttpRequest, id_usuario: int):

    if request.user.nivel_acesso != "ADMIN":
        return HttpResponseForbidden("Apenas admin pode promover usuários.")

    usuario = get_object_or_404(Usuarios, id_usuario=id_usuario)

    if usuario.nivel_acesso == "ADMIN":
        return HttpResponseForbidden("Não permitido alterar ADMIN.")

    if usuario.nivel_acesso == "USER":
        usuario.nivel_acesso = "STAFF"
        usuario.is_staff = True
    elif usuario.nivel_acesso == "STAFF":
        usuario.nivel_acesso = "USER"
        usuario.is_staff = False

    usuario.save()

    return redirect('administrador')
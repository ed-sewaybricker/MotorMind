from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpRequest, Http404
from django.contrib.auth.decorators import login_required

from ..models import Locais
from ..permissions import is_staff_or_admin

@login_required
def novo_local(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()

        if not nome:
            return redirect('locais')

        Locais.objects.create(nome=nome)
        return redirect('administrador')

    return redirect('administrador')


@login_required
def editar_local(request: HttpRequest, id_local: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    meuLocal = get_object_or_404(Locais, id_local=id_local)

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()

        if not nome:
            return redirect('administrador')

        meuLocal.nome = nome

        meuLocal.save()
        return redirect('administrador')

    return redirect('administrador')


@login_required
def deletar_local(request: HttpRequest, id_local: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    meuLocal = get_object_or_404(Locais, id_local=id_local)

    if request.method == 'POST':
        meuLocal.delete()
        return redirect('administrador')

    return redirect('administrador')
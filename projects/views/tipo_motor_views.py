from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpRequest, Http404

from django.contrib.auth.decorators import login_required

from ..models import TiposMotor
from ..permissions import is_staff_or_admin

@login_required
def novo_tipo_motor(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    if request.method == 'POST':

        descricao = request.POST.get('descricao', '').strip()

        if not descricao:
            return redirect('tipo_motor')

        TiposMotor.objects.create(descricao=descricao)

        return redirect('administrador')

    return redirect('administrador')


@login_required
def editar_tipo_motor(request: HttpRequest, id_tipo: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    meuTipoMotor = get_object_or_404(TiposMotor, id_tipo=id_tipo)

    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()

        if not descricao:
            return redirect('administrador')

        meuTipoMotor.descricao = descricao

        meuTipoMotor.save()

        return redirect('administrador')

    return redirect('administrador')


@login_required
def deletar_tipo_motor(request: HttpRequest, id_tipo: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    tipoMotor = get_object_or_404(TiposMotor, id_tipo=id_tipo)

    if request.method == 'POST':
        tipoMotor.delete()
        return redirect('administrador')

    return redirect('administrador')
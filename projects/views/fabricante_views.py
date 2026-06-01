from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, Http404

from ..models import Fabricantes
from ..permissions import is_staff_or_admin

@login_required
def novo_fabricante(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()

    # Essa view serve tanto para mostrar o formulário (GET)
    # quanto para salvar um novo fabricante (POST).
    if request.method == 'POST':

        # Pego o valor digitado no formulário.
        nome = request.POST.get('nome', '').strip()

        # Validação simples: se não tiver nome,
        # volta para a listagem.
        if not nome:
            return redirect('administrador')

        # Crio um novo registro no banco.
        Fabricantes.objects.create(nome=nome)

        # Depois de salvar,
        # redireciono para a lista.
        return redirect('administrador')

    # Se não for POST (ou seja, GET),
    # apenas mostro o formulário.
    return redirect('administrador')


@login_required
def editar_fabricante(request: HttpRequest, id_fabricante: int):

    if not is_staff_or_admin(request.user):
        raise Http404()

    # Busca o fabricante
    # ou retorna 404 se não existir
    fabricante = get_object_or_404(Fabricantes, id_fabricante=id_fabricante)

    if request.method == 'POST':
        # Pego o novo valor enviado pelo formulário.
        nome = request.POST.get('nome', '').strip()

        # Validação simples.
        if not nome:
            return redirect('administrador')

        # Atualizo o objeto com o novo valor.
        fabricante.nome = nome

        # Salvo a alteração no banco.
        fabricante.save()

        # Redireciono para a listagem.
        return redirect('administrador')

    # Se for GET, apenas exibo o formulário
    # com os dados atuais.
    return redirect('administrador')


@login_required
def deletar_fabricante(request: HttpRequest, id_fabricante: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    # Busco o fabricante pelo ID.
    fabricante = get_object_or_404(Fabricantes, id_fabricante=id_fabricante)

    if request.method == 'POST':

        # Deleto o registro do banco.
        fabricante.delete()

        # Após deletar,
        # volto para a listagem.
        return redirect('administrador')

    return redirect('administrador')
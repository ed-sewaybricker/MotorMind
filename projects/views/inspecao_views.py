from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, Http404, HttpResponseForbidden
from django.utils import timezone
from datetime import datetime

from ..permissions import is_staff_or_admin

from ..models import (
    Inspecoes,
    Motores,
    Usuarios
)

@login_required
def inspecoes(request: HttpRequest):

    if request.user.is_staff:
        inspecoes = Inspecoes.objects.select_related('id_motor', 'id_usuario').all()
    else:
        inspecoes = Inspecoes.objects.select_related('id_motor', 'id_usuario').filter(id_usuario=request.user)

    pendentes = inspecoes.filter(status='PENDENTE')
    em_andamento = inspecoes.filter(status='EM ANDAMENTO')
    concluidas = inspecoes.filter(status='CONCLUÍDO')

    usuarios = Usuarios.objects.all().order_by('nome')

    motores_em_inspecao = Inspecoes.objects.filter(status__in=['PENDENTE', 'EM ANDAMENTO']).values_list('id_motor_id', flat=True)

    motores = Motores.objects.exclude(id_motor__in=motores_em_inspecao).order_by('id_motor')

    return render(request, 'inspecoes.html', {
        'usuarios': usuarios,
        'motores': motores,
        'pendentes': pendentes,
        'em_andamento': em_andamento,
        'concluidas': concluidas
    })


@login_required
def nova_inspecao(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    if request.method == 'POST':
        motor_id = request.POST.get('motor')
        responsavel_id = request.POST.get('responsavel')
        data_inspecao = request.POST.get('data_inspecao')
        observacoes = request.POST.get('observacoes', '').strip()

        inspecao_aberta = Inspecoes.objects.filter(id_motor_id=motor_id,status__in=['PENDENTE', 'EM ANDAMENTO']).exists()

        if inspecao_aberta:
            return redirect('inspecoes')

        if not all([motor_id, responsavel_id, data_inspecao]):
            return redirect('inspecoes')

        Inspecoes.objects.create(
            id_motor_id=motor_id,
            id_usuario_id=responsavel_id,
            data_inspecao=data_inspecao,
            observacoes=observacoes,
            status='PENDENTE'
        )

        return redirect('inspecoes')

    return redirect('inspecoes')

@login_required
def iniciar_inspecao(request: HttpRequest, id_inspecao: int):

    inspecao = get_object_or_404(Inspecoes, id_inspecao=id_inspecao)

    if not request.user.is_staff and inspecao.id_usuario != request.user:
        return HttpResponseForbidden('Sem permissão.')

    if inspecao.status == 'PENDENTE':
        inspecao.status = 'EM ANDAMENTO'
        inspecao.data_inicio = timezone.now()
        inspecao.save()

    return redirect('inspecoes')

@login_required
def concluir_inspecao(request: HttpRequest, id_inspecao: int):

    inspecao = get_object_or_404(Inspecoes, id_inspecao=id_inspecao)

    if not request.user.is_staff and inspecao.id_usuario != request.user:
        return HttpResponseForbidden('Sem permissão.')

    if inspecao.status == 'EM ANDAMENTO':
        inspecao.status = 'CONCLUÍDO'
        inspecao.data_conclusao = timezone.now()
        inspecao.save()

    return redirect('inspecoes')


@login_required
def editar_inspecao(request: HttpRequest, id_inspecao: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    minhaInspecao = get_object_or_404(Inspecoes, id_inspecao=id_inspecao)

    motores = Motores.objects.all().order_by('modelo')

    if request.method == 'POST':
        motor_id = request.POST.get('motor')
        data_inspecao_str = request.POST.get('data_inspecao')
        observacoes = request.POST.get('observacoes', '').strip()

        if not observacoes:
            return redirect('editar_inspecao', id_inspecao=id_inspecao)

        if not data_inspecao_str:
            return redirect('editar_inspecao', id_inspecao=id_inspecao)

        data_inspecao = datetime.strptime(data_inspecao_str, '%Y-%m-%d').date()

        if motor_id:
            minhaInspecao.id_motor = Motores.objects.get(pk=motor_id)

        minhaInspecao.data_inspecao = data_inspecao
        minhaInspecao.observacoes = observacoes

        minhaInspecao.save()
        return redirect('inspecoes')

    return render(request, 'inspecoes/editar_inspecao.html', {
        'minhaInspecao': minhaInspecao,
        'motores': motores
    })


@login_required
def deletar_inspecao(request: HttpRequest, id_inspecao: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    minhaInspecao = get_object_or_404(Inspecoes, id_inspecao=id_inspecao)

    if request.method == 'POST':
        minhaInspecao.delete()
        return redirect('inspecoes')

    return render(request, 'inspecoes/confirmar_delete.html', {
        'minhaInspecao': minhaInspecao
    })
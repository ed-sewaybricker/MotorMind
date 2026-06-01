from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from ..models import Motores, Inspecoes

@login_required
def dashboard(request: HttpRequest):

    total_motores = Motores.objects.count()
    motores_em_manutencao = Inspecoes.objects.filter(status='EM ANDAMENTO').count()

    if request.user.is_staff:
        inspecoes_pendentes = Inspecoes.objects.filter(status='PENDENTE').count()
        ultimas_inspecoes = Inspecoes.objects.select_related('id_motor', 'id_usuario').order_by('-id_inspecao')[:10]

    else:
        inspecoes_pendentes = Inspecoes.objects.filter(status='PENDENTE', id_usuario=request.user).count()
        ultimas_inspecoes = Inspecoes.objects.select_related('id_motor','id_usuario').filter(id_usuario=request.user).order_by('-id_inspecao')[:10]

    return render(request, 'dashboard.html', {
        'total_motores': total_motores,
        'motores_em_manutencao': motores_em_manutencao,
        'inspecoes_pendentes': inspecoes_pendentes,
        'ultimas_inspecoes': ultimas_inspecoes
    })
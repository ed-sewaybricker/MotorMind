from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, Http404
from django.contrib.auth.decorators import login_required
from ..permissions import is_staff_or_admin

from ..models import (
    Motores,
    Fabricantes,
    TiposMotor,
    Locais
)

@login_required
def inventario(request: HttpRequest):

    meusMotores = Motores.objects.select_related('id_fabricante', 'id_tipo', 'id_local').all().order_by('id_motor')
    fabricantes = Fabricantes.objects.all().order_by('id_fabricante')
    tipos = TiposMotor.objects.all().order_by('id_tipo')
    locais = Locais.objects.all().order_by('id_local')

    return render(request, 'inventario.html', {
        'meusMotores': meusMotores,
        'fabricantes': fabricantes,
        'tipos': tipos,
        'locais': locais
    })


@login_required
def adicionar_motor(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    # Antes de tudo, busco os dados das tabelas relacionadas.
    # Esses dados serão usados para preencher os selects (dropdowns) no formulário.
    fabricantes = Fabricantes.objects.all().order_by('nome')
    tipos = TiposMotor.objects.all().order_by('descricao')
    locais = Locais.objects.all().order_by('nome')

    if request.method == 'POST':
        modelo = request.POST.get('modelo', '').strip()
        potencia = request.POST.get('potencia', '').strip()
        tensao = request.POST.get('tensao', '').strip()
        corrente = request.POST.get('corrente', '').strip()
        rpm = request.POST.get('rpm', '').strip()
        modo_fixacao = request.POST.get('modo_fixacao', '').strip()
        quantidade = request.POST.get('quantidade')

        quantidade = int(quantidade) if quantidade else 0
        if quantidade < 0:
            quantidade = 0

        # Pego os IDs das chaves estrangeiras
        # (vindos dos selects).
        fabricante_id = request.POST.get('fabricante')
        tipo_id = request.POST.get('tipo')
        local_id = request.POST.get('local')

        if not all([modelo, fabricante_id, tipo_id, local_id]):
            return redirect('inventario')

        # Para chaves estrangeiras,
        # posso usar diretamente o "_id"
        Motores.objects.create(
            modelo=modelo,
            potencia=potencia,
            tensao=tensao,
            corrente=corrente,
            rpm=rpm,
            modo_fixacao=modo_fixacao,
            quantidade=quantidade,
            id_fabricante_id=fabricante_id,
            id_tipo_id=tipo_id,
            id_local_id=local_id
        )

        return redirect('inventario')

    return render(request, 'motores/novo_motor.html', {
        'fabricantes': fabricantes,
        'tipos': tipos,
        'locais': locais
    })


@login_required
def editar_motor(request: HttpRequest, id_motor: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    meuMotor = get_object_or_404(Motores, id_motor=id_motor)

    if request.method == 'POST':

        modelo = request.POST.get('modelo', '').strip()
        potencia = request.POST.get('potencia', '').strip()
        tensao = request.POST.get('tensao', '').strip()
        corrente = request.POST.get('corrente', '').strip()
        rpm = request.POST.get('rpm', '').strip()
        modo_fixacao = request.POST.get('modo_fixacao', '').strip()
        quantidade = request.POST.get('quantidade')

        quantidade = int(quantidade) if quantidade else 0

        if quantidade < 0:
            quantidade = 0

        fabricante_id = request.POST.get('fabricante')
        tipo_id = request.POST.get('tipo')
        local_id = request.POST.get('local')

        if not all([modelo, fabricante_id, tipo_id, local_id]):
            return redirect('editar_motor', id_motor=id_motor)

        meuMotor.modelo = modelo
        meuMotor.potencia = potencia
        meuMotor.tensao = tensao
        meuMotor.corrente = corrente
        meuMotor.rpm = rpm
        meuMotor.modo_fixacao = modo_fixacao
        meuMotor.quantidade = quantidade

        meuMotor.id_fabricante_id = fabricante_id # type: ignore
        meuMotor.id_tipo_id = tipo_id # type: ignore
        meuMotor.id_local_id = local_id # type: ignore

        meuMotor.save()

        return redirect('inventario')

    return redirect('inventario')


@login_required
def excluir_motor(request: HttpRequest, id_motor: int):

    if not is_staff_or_admin(request.user):
        raise Http404()
    
    motor = get_object_or_404(Motores, id_motor=id_motor)

    if request.method == 'POST':
        motor.delete()
        return redirect('inventario')

    return redirect('inventario')
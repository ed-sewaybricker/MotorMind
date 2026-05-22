from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import (
    Fabricantes,
    TiposMotor,
    Locais,
    Motores,
    Inspecoes,
    Manutencoes
)
from datetime import datetime


def usuario_admin(request: HttpRequest):

    if not request.user.is_staff:
        return HttpResponseForbidden(
            'Você não possui permissão para acessar esta função.'
        )

    return None


# Este arquivo contém a lógica da aplicação.
# As funções (views) recebem requisições do usuário (request),
# processam dados (ex: buscar no banco, salvar, deletar)
# e retornam uma resposta.

def index(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        matricula = request.POST.get('matricula', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, matricula=matricula, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'index.html', {
            'erro': 'Matrícula ou senha inválidas'
        })

    return render(request, 'index.html')


@login_required
def dashboard(request: HttpRequest):
    return render(request, 'dashboard.html', {
        'usuario': request.user
    })


@login_required
def sair(request: HttpRequest):
    if request.method == 'POST':
        logout(request)
        return redirect('index')
    return redirect('dashboard')


'''
    FABRICANTES
'''

@login_required
def fabricantes(request: HttpRequest):

    # Aqui eu busco todos os fabricantes cadastrados no banco.
    meuFabricantes = Fabricantes.objects.all().order_by('nome')

    # Renderiza a página com os dados
    return render(request, 'fabricantes/fabricantes.html', {
        'meuFabricantes': meuFabricantes
    })


@login_required
def novo_fabricante(request: HttpRequest):

    # Essa view serve tanto para mostrar o formulário (GET)
    # quanto para salvar um novo fabricante (POST).

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    if request.method == 'POST':

        # Pego o valor digitado no formulário.
        nome = request.POST.get('nome', '').strip()

        # Validação simples: se não tiver nome,
        # volta para a listagem.
        if not nome:
            return redirect('fabricantes')

        # Crio um novo registro no banco.
        Fabricantes.objects.create(nome=nome)

        # Depois de salvar,
        # redireciono para a lista.
        return redirect('fabricantes')

    # Se não for POST (ou seja, GET),
    # apenas mostro o formulário.
    return render(request, 'fabricantes/novo_fabricante.html')


@login_required
def editar_fabricante(request: HttpRequest, id_fabricante: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    # Busca o fabricante
    # ou retorna 404 se não existir
    meuFabricante = get_object_or_404(Fabricantes, id_fabricante=id_fabricante)

    if request.method == 'POST':
        # Pego o novo valor enviado pelo formulário.
        nome = request.POST.get('nome', '').strip()

        # Validação simples.
        if not nome:
            return redirect('fabricantes')

        # Atualizo o objeto com o novo valor.
        meuFabricante.nome = nome

        # Salvo a alteração no banco.
        meuFabricante.save()

        # Redireciono para a listagem.
        return redirect('fabricantes')

    # Se for GET, apenas exibo o formulário
    # com os dados atuais.
    return render(request, 'fabricantes/editar_fabricante.html', {
        'meuFabricante': meuFabricante
    })


@login_required
def deletar_fabricante(request: HttpRequest, id_fabricante: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    # Busco o fabricante pelo ID.
    meuFabricante = get_object_or_404(Fabricantes, id_fabricante=id_fabricante)

    if request.method == 'POST':

        # Deleto o registro do banco.
        meuFabricante.delete()

        # Após deletar,
        # volto para a listagem.
        return redirect('fabricantes')

    return render(request, 'fabricantes/confirmar_delete.html', {
        'meuFabricante': meuFabricante
    })


'''
    TIPOS DE MOTORES
'''

@login_required
def tipo_motor(request: HttpRequest):

    meuTipoMotor = TiposMotor.objects.all().order_by('descricao')

    return render(request, 'tipomotor/tipomotor.html', {
        'meuTipoMotor': meuTipoMotor
    })


@login_required
def novo_tipo_motor(request: HttpRequest):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    if request.method == 'POST':

        descricao = request.POST.get('descricao', '').strip()

        if not descricao:
            return redirect('tipo_motor')

        TiposMotor.objects.create(descricao=descricao)

        return redirect('tipo_motor')

    return render(request, 'tipomotor/novo_tipo_motor.html')


@login_required
def editar_tipo_motor(request: HttpRequest, id_tipo: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    meuTipoMotor = get_object_or_404(TiposMotor, id_tipo=id_tipo)

    if request.method == 'POST':
        descricao = request.POST.get('descricao', '').strip()

        if not descricao:
            return redirect('tipo_motor')

        meuTipoMotor.descricao = descricao

        meuTipoMotor.save()

        return redirect('tipo_motor')

    return render(request, 'tipomotor/editar_tipo_motor.html', {
        'meuTipoMotor': meuTipoMotor
    })


@login_required
def deletar_tipo_motor(request: HttpRequest, id_tipo: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    tipoMotor = get_object_or_404(TiposMotor, id_tipo=id_tipo)

    if request.method == 'POST':
        tipoMotor.delete()
        return redirect('tipo_motor')

    return render(request, 'tipomotor/confirmar_delete.html', {
        'tipoMotor': tipoMotor
    })


'''
    LOCAIS
'''

@login_required
def locais(request: HttpRequest):

    meusLocais = Locais.objects.all().order_by('nome')

    return render(request, 'locais/locais.html', {
        'meusLocais': meusLocais
    })


@login_required
def novo_local(request: HttpRequest):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()

        if not nome:
            return redirect('locais')

        Locais.objects.create(nome=nome)
        return redirect('locais')

    return render(request, 'locais/novo_local.html')


@login_required
def editar_local(request: HttpRequest, id_local: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    meuLocal = get_object_or_404(Locais, id_local=id_local)

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()

        if not nome:
            return redirect('locais')

        meuLocal.nome = nome

        meuLocal.save()
        return redirect('locais')

    return render(request, 'locais/editar_local.html', {
        'meuLocal': meuLocal
    })


@login_required
def deletar_local(request: HttpRequest, id_local: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    meuLocal = get_object_or_404(Locais, id_local=id_local)

    if request.method == 'POST':
        meuLocal.delete()
        return redirect('locais')

    return render(request, 'locais/confirmar_delete.html', {
        'meuLocal': meuLocal
    })


'''
    MOTORES
'''

@login_required
def motores(request: HttpRequest):

    meusMotores = Motores.objects.select_related('id_fabricante', 'id_tipo', 'id_local').all().order_by('modelo')

    return render(request, 'motores/motores.html', {
        'meusMotores': meusMotores
    })


@login_required
def novo_motor(request: HttpRequest):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

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

        # Pego os IDs das chaves estrangeiras
        # (vindos dos selects).
        fabricante_id = request.POST.get('fabricante')
        tipo_id = request.POST.get('tipo')
        local_id = request.POST.get('local')

        if not all([modelo, fabricante_id, tipo_id, local_id]):
            return redirect('novo_motor')

        # Para chaves estrangeiras,
        # posso usar diretamente o "_id"
        Motores.objects.create(
            modelo=modelo,
            potencia=potencia,
            tensao=tensao,
            corrente=corrente,
            rpm=rpm,
            modo_fixacao=modo_fixacao,
            id_fabricante_id=fabricante_id,
            id_tipo_id=tipo_id,
            id_local_id=local_id
        )

        return redirect('motores')

    return render(request, 'motores/novo_motor.html', {
        'fabricantes': fabricantes,
        'tipos': tipos,
        'locais': locais
    })


@login_required
def editar_motor(request: HttpRequest, id_motor: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    meuMotor = get_object_or_404(Motores, id_motor=id_motor)

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

        meuMotor.id_fabricante_id = fabricante_id
        meuMotor.id_tipo_id = tipo_id
        meuMotor.id_local_id = local_id

        meuMotor.save()

        return redirect('motores')

    return render(request, 'motores/editar_motor.html', {
        'meuMotor': meuMotor,
        'fabricantes': fabricantes,
        'tipos': tipos,
        'locais': locais
    })


@login_required
def deletar_motor(request: HttpRequest, id_motor: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    motor = get_object_or_404(Motores, id_motor=id_motor)

    if request.method == 'POST':
        motor.delete()
        return redirect('motores')

    return render(request, 'motores/confirmar_delete.html', {
        'motor': motor
    })


'''
    INSPEÇÕES
'''

@login_required
def inspecoes(request: HttpRequest):

    minhasInspecoes = Inspecoes.objects.select_related('id_motor').all().order_by('-data_inspecao')

    return render(request, 'inspecoes/inspecoes.html', {
        'minhasInspecoes': minhasInspecoes
    })


@login_required
def nova_inspecao(request: HttpRequest):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    motores = Motores.objects.all().order_by('modelo')

    if request.method == 'POST':
        motor_id = request.POST.get('motor')
        data_inspecao = request.POST.get('data_inspecao')
        observacoes = request.POST.get('observacoes', '').strip()

        if not all([motor_id, data_inspecao, observacoes]):
            return redirect('nova_inspecao')

        Inspecoes.objects.create(
            id_motor_id=motor_id,
            id_usuario=request.user,
            data_inspecao=data_inspecao,
            observacoes=observacoes
        )

        return redirect('inspecoes')

    return render(request, 'inspecoes/nova_inspecao.html', {
        'motores': motores
    })


@login_required
def editar_inspecao(request: HttpRequest, id_inspecao: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

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
            minhaInspecao.id_motor_id = motor_id

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

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    minhaInspecao = get_object_or_404(Inspecoes, id_inspecao=id_inspecao)

    if request.method == 'POST':
        minhaInspecao.delete()
        return redirect('inspecoes')

    return render(request, 'inspecoes/confirmar_delete.html', {
        'minhaInspecao': minhaInspecao
    })


'''
    MANUTENÇÕES
'''

@login_required
def manutencoes(request: HttpRequest):

    minhasManutencoes = Manutencoes.objects.select_related('id_motor').all().order_by('-data_manutencao')

    return render(request, 'manutencoes/manutencoes.html', {
        'minhasManutencoes': minhasManutencoes
    })


@login_required
def nova_manutencao(request: HttpRequest):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    motores = Motores.objects.all().order_by('modelo')

    if request.method == 'POST':
        motor_id = request.POST.get('motor')
        tipo = request.POST.get('tipo', '').strip()
        data_manutencao = request.POST.get('data_manutencao')
        descricao = request.POST.get('descricao', '').strip()

        if not all([motor_id, tipo, data_manutencao, descricao]):
            return redirect('nova_manutencao')

        Manutencoes.objects.create(
            id_motor_id=motor_id,
            id_usuario=request.user,
            tipo=tipo,
            data_manutencao=data_manutencao,
            descricao=descricao
        )

        return redirect('manutencoes')

    return render(request, 'manutencoes/nova_manutencao.html', {
        'motores': motores
    })


@login_required
def editar_manutencao(request: HttpRequest, id_manutencao: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    minhaManutencao = get_object_or_404(Manutencoes, id_manutencao=id_manutencao)

    motores = Motores.objects.all().order_by('modelo')

    if request.method == 'POST':
        motor_id = request.POST.get('motor')
        tipo = request.POST.get('tipo', '').strip()
        data_manutencao_str = request.POST.get('data_manutencao')
        descricao = request.POST.get('descricao', '').strip()

        if not descricao:
            return redirect('editar_manutencao', id_manutencao=id_manutencao)

        if not data_manutencao_str:
            return redirect('editar_manutencao', id_manutencao=id_manutencao)

        data_manutencao = datetime.strptime(data_manutencao_str, '%Y-%m-%d').date()

        if motor_id:
            minhaManutencao.id_motor = motor_id

        minhaManutencao.tipo = tipo
        minhaManutencao.data_manutencao = data_manutencao
        minhaManutencao.descricao = descricao

        minhaManutencao.save()
        return redirect('manutencoes')

    return render(request, 'manutencoes/editar_manutencao.html', {
        'minhaManutencao': minhaManutencao,
        'motores': motores
    })


@login_required
def deletar_manutencao(request: HttpRequest, id_manutencao: int):

    permissao = usuario_admin(request)

    if permissao:
        return permissao

    minhaManutencao = get_object_or_404(Manutencoes, id_manutencao=id_manutencao)

    if request.method == 'POST':
        minhaManutencao.delete()
        return redirect('manutencoes')

    return render(request, 'manutencoes/confirmar_delete.html', {
        'minhaManutencao': minhaManutencao
    })
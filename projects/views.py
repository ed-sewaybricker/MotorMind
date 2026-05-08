from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.template import loader
from .models import Fabricantes, TiposMotor, Locais, Motores, Inspecoes, Manutencoes #type:ignore
from datetime import datetime

# Este arquivo contém a lógica da aplicação.
# As funções (views) recebem requisições do usuário (request),
# processam dados (ex: buscar no banco, salvar, deletar)
# e retornam uma resposta.

def index(request: HttpRequest):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

'''
    FABRICANTES
'''

def fabricantes(request: HttpRequest):
    # Aqui eu busco todos os fabricantes cadastrados no banco.
    # O .values() transforma os dados em dicionário (facilita usar no template).
    meuFabricantes = Fabricantes.objects.all()

    # Renderiza a página com os dados
    return render(request, 'fabricantes/fabricantes.html', {
        'meuFabricantes': meuFabricantes
    })

def novo_fabricante(request: HttpRequest):
    # Essa view serve tanto para mostrar o formulário (GET)
    # quanto para salvar um novo fabricante (POST).

    if request.method == 'POST':
        # Pego o valor digitado no formulário.
        nome = request.POST.get('nome')

        # Validação simples: se não tiver nome, volta para a listagem.
        if not nome:
            return redirect('fabricantes')
        
        # Crio um novo registro no banco.
        Fabricantes.objects.create(nome=nome)

        # Depois de salvar, redireciono para a lista.
        return redirect('fabricantes')
    
    # Se não for POST (ou seja, GET), apenas mostro o formulário.
    return render(request, 'fabricantes/novo_fabricante.html')

def editar_fabricante(request: HttpRequest, id_fabricante: int):
    # Busca o fabricante ou retorna 404 se não existir
    meuFabricante = get_object_or_404(Fabricantes, id_fabricante=id_fabricante)

    if request.method == 'POST':
        # Pego o novo valor enviado pelo formulário.
        nome = request.POST.get('nome')

        # Validação simples.
        if not nome:
            return redirect('fabricantes')

        # Atualizo o objeto com o novo valor.
        meuFabricante.nome = nome

        # Salvo a alteração no banco.
        meuFabricante.save()

        # Redireciono para a listagem.
        return redirect('fabricantes')

    # Se for GET, apenas exibo o formulário com os dados atuais.
    return render(request, 'fabricantes/editar_fabricante.html', {
        'meuFabricante': meuFabricante
    })

def deletar_fabricante(request: HttpRequest, id_fabricante: int):
    # Busco o fabricante pelo ID.
    meuFabricante = get_object_or_404(Fabricantes, id_fabricante=id_fabricante)

    # Deleto o registro do banco.
    meuFabricante.delete()

    # Após deletar, volto para a listagem.
    return redirect('fabricantes')

'''
    TIPOS DE MOTORES
'''

def tipo_motor(request: HttpRequest):

    meuTipoMotor = TiposMotor.objects.all()

    return render(request, 'tipomotor/tipomotor.html', {
        'meuTipoMotor': meuTipoMotor
    })

def novo_tipo_motor(request: HttpRequest):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')

        if not descricao:
            return redirect('tipo_motor')
        
        TiposMotor.objects.create(descricao=descricao)

        return redirect('tipo_motor')
    
    return render(request, 'tipomotor/novo_tipo_motor.html')
    
def editar_tipo_motor(request: HttpRequest, id_tipo: int):
    meuTipoMotor = get_object_or_404(TiposMotor, id_tipo=id_tipo)

    if request.method == 'POST':
        descricao = request.POST.get('descricao')

        if not descricao:
            return redirect('tipo_motor')

        meuTipoMotor.descricao = descricao
        meuTipoMotor.save()

        return redirect('tipo_motor')

    return render(request, 'tipomotor/editar_tipo_motor.html', {
        'meuTipoMotor': meuTipoMotor
    })

def deletar_tipo_motor(request: HttpRequest, id_tipo: int):
    tipoMotor = get_object_or_404(TiposMotor, id_tipo=id_tipo)
    tipoMotor.delete()
    return redirect('tipo_motor')

'''
    LOCAIS
'''

def locais(request: HttpRequest):
    meusLocais = Locais.objects.all()
    return render(request, 'locais/locais.html', {'meusLocais' : meusLocais,})

def novo_local(request: HttpRequest):
    if request.method == 'POST':
        nome = request.POST.get('nome')

        if not nome:
            return redirect('locais')
        
        Locais.objects.create(nome=nome)

        return redirect('locais')
    
    return render(request, 'locais/novo_local.html')
    
def editar_local(request: HttpRequest, id_local: int):
    meuLocal = get_object_or_404(Locais, id_local=id_local)

    if request.method == 'POST':
        nome = request.POST.get('nome')

        if not nome:
            return redirect('locais')

        meuLocal.nome = nome
        meuLocal.save()

        return redirect('locais')

    return render(request, 'locais/editar_local.html', {'meuLocal': meuLocal})

def deletar_local(request: HttpRequest, id_local: int):
    meuLocal = get_object_or_404(Locais, id_local=id_local)
    meuLocal.delete()
    return redirect('locais')

'''
    MOTORES
'''

def motores(request: HttpRequest):
    meusMotores = Motores.objects.select_related('id_fabricante', 'id_tipo', 'id_local').all()
    return render(request, 'motores/motores.html', {'meusMotores' : meusMotores,})

def novo_motor(request: HttpRequest):

    # Antes de tudo, busco os dados das tabelas relacionadas.
    # Esses dados serão usados para preencher os selects (dropdowns) no formulário.
    fabricantes = Fabricantes.objects.all() #type:ignore
    tipos = TiposMotor.objects.all() #type:ignore
    locais = Locais.objects.all() #type:ignore

    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        potencia = request.POST.get('potencia')
        tensao = request.POST.get('tensao')
        corrente = request.POST.get('corrente')
        rpm = request.POST.get('rpm')
        modo_fixacao = request.POST.get('modo_fixacao')

        # Pego os IDs das chaves estrangeiras (vindos dos selects).
        fabricante_id = request.POST.get('fabricante')
        tipo_id = request.POST.get('tipo')
        local_id = request.POST.get('local')

        if not all([modelo, fabricante_id, tipo_id, local_id]):
            return redirect('novo_motor')
    
        # Para chaves estrangeiras, posso usar diretamente o "_id" (frescura do Django que não sei explicar porque).
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
    
def editar_motor(request: HttpRequest, id_motor: int):
    meuMotor = get_object_or_404(Motores, id_motor=id_motor)

    fabricantes = Fabricantes.objects.all()
    tipos = TiposMotor.objects.all()
    locais = Locais.objects.all()

    if request.method == 'POST':
        modelo = request.POST.get('modelo') or ''
        potencia = request.POST.get('potencia') or ''
        tensao = request.POST.get('tensao') or ''
        corrente = request.POST.get('corrente') or ''
        rpm = request.POST.get('rpm') or ''
        modo_fixacao = request.POST.get('modo_fixacao') or ''

        fabricante_id = request.POST.get('fabricante')
        tipo_id = request.POST.get('tipo')
        local_id = request.POST.get('local')

        if not modelo:
            return redirect('editar_motor', id_motor=id_motor)

        meuMotor.modelo = modelo
        meuMotor.potencia = potencia
        meuMotor.tensao = tensao
        meuMotor.corrente = corrente
        meuMotor.rpm = rpm
        meuMotor.modo_fixacao = modo_fixacao

        if fabricante_id:
            meuMotor.id_fabricante = Fabricantes.objects.get(id_fabricante=fabricante_id)

        if tipo_id:
            meuMotor.id_tipo = TiposMotor.objects.get(id_tipo=tipo_id)

        if local_id:
            meuMotor.id_local = Locais.objects.get(id_local=local_id)

        meuMotor.save()

        return redirect('motores')

    return render(request, 'motores/editar_motor.html', {
        'meuMotor': meuMotor,
        'fabricantes': fabricantes,
        'tipos': tipos,
        'locais': locais,
    })

def deletar_motor(request: HttpRequest, id_motor: int):
    motor = get_object_or_404(Motores, id_motor=id_motor)
    motor.delete()
    return redirect('motores')

'''
    INSPEÇÕES
'''

def inspecoes(request: HttpRequest):
    
    minhasInspecoes = Inspecoes.objects.select_related(
        'id_motor'
    ).all()

    return render(request, 'inspecoes/inspecoes.html', {
        'minhasInspecoes': minhasInspecoes
    })

def nova_inspecao(request: HttpRequest):
    
    motores = Motores.objects.all()

    if request.method == 'POST':

        motor_id = request.POST.get('motor')
        data_inspecao = request.POST.get('data_inspecao')
        observacoes = request.POST.get('observacoes')

        if not all([
            motor_id,
            data_inspecao,
            observacoes
        ]):
            return redirect('nova_inspecao')

        Inspecoes.objects.create(
            id_motor_id=motor_id,
            data_inspecao=data_inspecao,
            observacoes=observacoes
        )

        return redirect('inspecoes')

    return render(request, 'inspecoes/nova_inspecao.html', {
        'motores': motores
    })
    
def editar_inspecao(request: HttpRequest, id_inspecao: int):
    
    minhaInspecao = get_object_or_404(
        Inspecoes,
        id_inspecao=id_inspecao
    )

    motores = Motores.objects.all()

    if request.method == 'POST':

        motor_id = request.POST.get('motor')
        data_inspecao_str = request.POST.get('data_inspecao')
        observacoes = request.POST.get('observacoes') or ''

        if not observacoes:
            return redirect(
                'editar_inspecao',
                id_inspecao=id_inspecao
            )
        
        if not data_inspecao_str:
            return redirect('editar_inspecao', id_inspecao=id_inspecao)
        
        data_inspecao = datetime.strptime(data_inspecao_str, '%Y-%m-%d').date()

        if motor_id:
            minhaInspecao.id_motor = Motores.objects.get(
                id_motor=motor_id
            )

        minhaInspecao.data_inspecao = data_inspecao
        minhaInspecao.observacoes = observacoes

        minhaInspecao.save()

        return redirect('inspecoes')

    return render(request, 'inspecoes/editar_inspecao.html', {
        'minhaInspecao': minhaInspecao,
        'motores': motores
    })

def deletar_inspecao(request: HttpRequest, id_inspecao: int):
    
    minhaInspecao = get_object_or_404(
        Inspecoes,
        id_inspecao=id_inspecao
    )

    minhaInspecao.delete()

    return redirect('inspecoes')

'''
    MANUTENÇÕES
'''

def manutencoes(request: HttpRequest):
    
    minhasManutencoes = Manutencoes.objects.select_related(
        'id_motor'
    ).all()

    return render(request, 'manutencoes/manutencoes.html', {
        'minhasManutencoes': minhasManutencoes
    })

def nova_manutencao(request: HttpRequest):
    
    motores = Motores.objects.all()

    if request.method == 'POST':

        motor_id = request.POST.get('motor')
        tipo = request.POST.get('tipo')
        data_manutencao = request.POST.get('data_manutencao')
        descricao = request.POST.get('descricao')

        if not all([
            motor_id,
            tipo,
            data_manutencao,
            descricao
        ]):
            return redirect('nova_manutencao')

        Manutencoes.objects.create(
            id_motor_id=motor_id,
            tipo=tipo,
            data_manutencao=data_manutencao,
            descricao=descricao
        )

        return redirect('manutencoes')

    return render(request, 'manutencoes/nova_manutencao.html', {
        'motores': motores
    })
    
def editar_manutencao(request: HttpRequest, id_manutencao: int):
    
    minhaManutencao = get_object_or_404(
        Manutencoes,
        id_manutencao=id_manutencao
    )

    motores = Motores.objects.all()

    if request.method == 'POST':

        motor_id = request.POST.get('motor')
        tipo = request.POST.get('tipo') or ''
        data_manutencao_str = request.POST.get('data_manutencao')
        descricao = request.POST.get('descricao') or ''

        if not descricao:
            return redirect(
                'editar_manutencao',
                id_manutencao=id_manutencao
            )
        
        if not data_manutencao_str:
            return redirect(
                'editar_manutencao',
                id_manutencao=id_manutencao
            )
        
        data_manutencao = datetime.strptime(data_manutencao_str, '%Y-%m-%d').date()

        if motor_id:
            minhaManutencao.id_motor = Motores.objects.get(
                id_motor=motor_id
            )

        minhaManutencao.tipo = tipo
        minhaManutencao.data_manutencao = data_manutencao
        minhaManutencao.descricao = descricao

        minhaManutencao.save()

        return redirect('manutencoes')

    return render(request, 'manutencoes/editar_manutencao.html', {
        'minhaManutencao': minhaManutencao,
        'motores': motores
    })

def deletar_manutencao(request: HttpRequest, id_manutencao: int):
    
    minhaManutencao = get_object_or_404(
        Manutencoes,
        id_manutencao=id_manutencao
    )

    minhaManutencao.delete()

    return redirect('manutencoes')
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseForbidden, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from datetime import datetime
from .models import Usuarios

from .models import (
    Fabricantes,
    TiposMotor,
    Locais,
    Motores,
    Inspecoes,
    Usuarios
)

def is_admin(user):
    return user.is_authenticated and user.nivel_acesso == "ADMIN"

def is_staff_or_admin(user):
    return user.is_authenticated and user.nivel_acesso in ["ADMIN", "STAFF"]

def is_user(user):
    return user.is_authenticated and user.nivel_acesso == "USER"


def deny_if_not(condition, message="Sem permissão"):
    if not condition:
        return HttpResponseForbidden(message)
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

@login_required
def administrador(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()

    fabricantes = Fabricantes.objects.all().order_by('nome')
    tipos = TiposMotor.objects.all().order_by('descricao')
    locais = Locais.objects.all().order_by('nome')

    if request.user.nivel_acesso == "ADMIN":
        usuarios = Usuarios.objects.all().order_by("id_usuario")
        pode_promover = True
    else:
        usuarios = Usuarios.objects.exclude(nivel_acesso="ADMIN").order_by("id_usuario")
        pode_promover = False

    return render(request, 'administrador.html', {
        'usuarios': usuarios,
        'pode_promover': pode_promover,
        'fabricantes': fabricantes,
        'tipos': tipos,
        'locais': locais
    })

'''
    USUÁRIOS
'''

@login_required
def usuarios(request: HttpRequest):
    
    if not is_staff_or_admin(request.user):
        raise Http404()

    usuarios = Usuarios.objects.all().order_by('nome')

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

        if is_admin(request.user):
            nivel = request.POST.get('nivel_acesso')

            if nivel in ["STAFF", "USER"]:
                usuario.nivel_acesso = nivel
            else:
                usuario.nivel_acesso = "USER"
        else:
            usuario.nivel_acesso = "USER"

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
        usuario.matricula = request.POST.get('matricula', '').strip()

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
    elif usuario.nivel_acesso == "STAFF":
        usuario.nivel_acesso = "USER"

    usuario.save()

    return redirect('administrador')

'''
    FABRICANTES
'''

@login_required
def fabricantes(request: HttpRequest):

    if not request.user.is_staff:
        raise Http404()

    # Aqui eu busco todos os fabricantes cadastrados no banco.
    meuFabricantes = Fabricantes.objects.all().order_by('nome')

    # Renderiza a página com os dados
    return render(request, 'fabricantes/fabricantes.html', {
        'meuFabricantes': meuFabricantes
    })


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


'''
    TIPOS DE MOTORES
'''

@login_required
def tipo_motor(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()

    meuTipoMotor = TiposMotor.objects.all().order_by('id_tipo')

    return render(request, 'tipomotor/tipomotor.html', {
        'meuTipoMotor': meuTipoMotor
    })


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


'''
    LOCAIS
'''

@login_required
def locais(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()

    meusLocais = Locais.objects.all().order_by('nome')

    return render(request, 'locais/locais.html', {
        'meusLocais': meusLocais
    })


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


'''
    MOTORES
'''

@login_required
def inventario(request: HttpRequest):

    meusMotores = Motores.objects.select_related('id_fabricante', 'id_tipo', 'id_local').all().order_by('modelo')
    fabricantes = Fabricantes.objects.all().order_by('nome')
    tipos = TiposMotor.objects.all().order_by('descricao')
    locais = Locais.objects.all().order_by('nome')

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


'''
    INSPEÇÕES
'''

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

    motores = Motores.objects.exclude(id_motor__in=motores_em_inspecao).order_by('modelo')

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
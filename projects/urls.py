from django.urls import path
from . import views

# Este arquivo define as rotas da aplicação.
# Ele conecta uma URL (endereço no navegador)
# a uma função no views.py.
# Também define nomes para as rotas (name=),
# que são usados nos templates com {% url %}.

urlpatterns = [
    path('', views.index, name='index'),
    path('alterar-senha/', views.alterar_senha_obrigatoria, name='alterar_senha_obrigatoria'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sair/', views.sair, name='sair'),

    path('administrador/', views.administrador, name='administrador'),

    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/adicionar', views.novo_usuario, name='novo_usuario'),
    path('usuarios/editar/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/deletar/<int:id_usuario>/', views.deletar_usuario, name='deletar_usuario'),
    path('usuarios/reset/<int:id_usuario>/', views.reset, name='reset'),
    path('usuarios/promover/<int:id_usuario>/', views.promover, name='promover'),

    path('inventario/', views.inventario, name='inventario'),
    path('inventario/adicionar/', views.adicionar_motor, name='adicionar_motor'),
    path('inventario/editar/<int:id_motor>', views.editar_motor, name='editar_motor'),
    path('inventario/excluir/<int:id_motor>', views.excluir_motor, name='excluir_motor'),

    path('inspecoes/', views.inspecoes, name='inspecoes'),
    path('inspecoes/nova/', views.nova_inspecao, name='nova_inspecao'),
    path('inspecoes/iniciar/<int:id_inspecao>/', views.iniciar_inspecao, name='iniciar_inspecao'),
    path('inspecoes/concluir/<int:id_inspecao>/', views.concluir_inspecao, name='concluir_inspecao'),

    path('fabricantes/', views.fabricantes, name='fabricantes'),
    path('fabricantes/novo/', views.novo_fabricante, name='novo_fabricante'),
    path('fabricantes/editar/<int:id_fabricante>/', views.editar_fabricante, name='editar_fabricante'),
    path('fabricantes/deletar/<int:id_fabricante>/', views.deletar_fabricante, name='deletar_fabricante'),

    path('tipos-motor/', views.tipo_motor, name='tipo_motor'),
    path('tipos-motor/novo/', views.novo_tipo_motor, name='novo_tipo_motor'),
    path('tipos-motor/editar/<int:id_tipo>/', views.editar_tipo_motor, name='editar_tipo_motor'),
    path('tipos-motor/deletar/<int:id_tipo>/', views.deletar_tipo_motor, name='deletar_tipo_motor'),

    path('locais/', views.locais, name='locais'),
    path('locais/novo/', views.novo_local, name='novo_local'),
    path('locais/editar/<int:id_local>/', views.editar_local, name='editar_local'),
    path('locais/deletar/<int:id_local>/', views.deletar_local, name='deletar_local'),
]

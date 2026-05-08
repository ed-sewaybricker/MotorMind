from django.urls import path
from . import views

# Este arquivo define as rotas da aplicação.
# Ele conecta uma URL (endereço no navegador)
# a uma função no views.py.
# Também define nomes para as rotas (name=),
# que são usados nos templates com {% url %}.

urlpatterns = [
    path('', views.index, name='index'),
    # FABRICANTES
    path('fabricantes', views.fabricantes, name='fabricantes'),
    path('fabricante/novo_fabricante', views.novo_fabricante, name='novo_fabricante'),
    path('fabricante/editar_fabricante/<int:id_fabricante>', views.editar_fabricante, name='editar_fabricante'),
    path('fabricantes/deletar_fabricante/<int:id_fabricante>', views.deletar_fabricante, name='deletar_fabricante'),
    # TIPOS DE MOTORES
    path('tipo_motor', views.tipo_motor, name='tipo_motor'),
    path('tipo_motor/novo_tipo_motor', views.novo_tipo_motor, name='novo_tipo_motor'),
    path('tipo_motor/editar_tipo_motor/<int:id_tipo>', views.editar_tipo_motor, name='editar_tipo_motor'),
    path('tipo_motor/deletar_tipo_motor/<int:id_tipo>', views.deletar_tipo_motor, name='deletar_tipo_motor'),
    # LOCAIS
    path('locais', views.locais, name='locais'),
    path('locais/novo_local', views.novo_local, name='novo_local'),
    path('locais/editar_local/<int:id_local>', views.editar_local, name='editar_local'),
    path('locais/deletar_local/<int:id_local>', views.deletar_local, name='deletar_local'),
    # MOTORES
    path('motores', views.motores, name='motores'),
    path('motores/novo_motor', views.novo_motor, name='novo_motor'),
    path('motores/editar_motor/<int:id_motor>', views.editar_motor, name='editar_motor'),
    path('motores/deletar_motor/<int:id_motor>', views.deletar_motor, name='deletar_motor'),
    # INSPEÇÕES
    path('inspecoes', views.inspecoes, name='inspecoes'),
    path('inspecoes/nova_inspecao', views.nova_inspecao, name='nova_inspecao'),
    path('inspecoes/editar_inspecao/<int:id_inspecao>', views.editar_inspecao, name='editar_inspecao'),
    path('inspecoes/deletar_inspecao/<int:id_inspecao>', views.deletar_inspecao, name='deletar_inspecao'),
    # MANUTENÇÕES
    path('manutencoes', views.manutencoes, name='manutencoes'),
    path('manutencoes/nova_manutencao', views.nova_manutencao, name='nova_manutencao'),
    path('manutencoes/editar_manutencao/<int:id_manutencao>', views.editar_manutencao, name='editar_manutencao'),
    path('manutencoes/deletar_manutencao/<int:id_manutencao>', views.deletar_manutencao, name='deletar_manutencao'),
]

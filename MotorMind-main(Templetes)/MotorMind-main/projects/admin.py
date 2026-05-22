from django.contrib import admin
from .models import Fabricantes, TiposMotor, Locais, Usuarios, Motores, Inspecoes, Manutencoes

# Aqui a gente registra os models para aparecerem no painel administrativo do Django.
# Facilita visualizar, editar e deletar dados.

# class FabricantesAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'telefone', 'idade')

# admin.site.register(Fabricantes, FabricantesAdmin)
admin.site.register(Fabricantes)
admin.site.register(TiposMotor)
admin.site.register(Locais)
admin.site.register(Usuarios)
admin.site.register(Motores)
admin.site.register(Inspecoes)
admin.site.register(Manutencoes)

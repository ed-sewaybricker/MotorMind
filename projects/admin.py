from django.contrib import admin
from .models import Fabricantes, TiposMotor, Locais, Usuarios, Motores, Inspecoes
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios

@admin.register(Usuarios)
class UsuariosAdmin(UserAdmin):

    model = Usuarios

    ordering = ('matricula',)

    list_display = ('matricula', 'nome', 'is_staff', 'is_superuser', 'is_active')

    search_fields = ('matricula', 'nome')

    fieldsets = (
        (None, {
            'fields': ('matricula', 'password')
        }),

        ('Informações pessoais', {
            'fields': ('nome',)
        }),

        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricula', 'nome', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active'
            ),
        }),
    )

# Aqui a gente registra os models para aparecerem no painel administrativo do Django.
# Facilita visualizar, editar e deletar dados.

# class FabricantesAdmin(admin.ModelAdmin):
#     list_display = ('nome', 'telefone', 'idade')

# admin.site.register(Fabricantes, FabricantesAdmin)
admin.site.register(Fabricantes)
admin.site.register(TiposMotor)
admin.site.register(Locais)
admin.site.register(Motores)
admin.site.register(Inspecoes)

from django.contrib import admin
from .models import Fabricantes, TiposMotor, Locais, Usuarios, Motores, Inspecoes, Manutencoes
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios

@admin.register(Usuarios)
class UsuariosAdmin(UserAdmin):

    ordering = ('matricula',)

    list_display = (
        'matricula',
        'is_staff',
        'is_superuser',
        'is_active'
    )

    search_fields = ('matricula',)

    fieldsets = (
        (None, {
            'fields': (
                'matricula',
                'password'
            )
        }),

        ('Permissões', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'matricula',
                'password1',
                'password2',
                'is_staff',
                'is_superuser'
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
admin.site.register(Manutencoes)

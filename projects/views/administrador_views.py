from django.shortcuts import render
from django.http import HttpRequest, Http404

from django.contrib.auth.decorators import login_required

from ..models import Usuarios, Fabricantes, TiposMotor, Locais
from ..permissions import is_staff_or_admin

@login_required
def administrador(request: HttpRequest):

    if not is_staff_or_admin(request.user):
        raise Http404()

    fabricantes = Fabricantes.objects.all().order_by('id_fabricante')
    tipos = TiposMotor.objects.all().order_by('id_tipo')
    locais = Locais.objects.all().order_by('id_local')

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
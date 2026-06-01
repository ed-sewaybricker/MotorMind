from typing import Any
from django.http import HttpResponseForbidden

def is_admin(user: Any):
    return user.is_authenticated and user.nivel_acesso == "ADMIN"

def is_staff_or_admin(user: Any):
    return user.is_authenticated and user.nivel_acesso in ["ADMIN", "STAFF"]

def is_user(user: Any):
    return user.is_authenticated and user.nivel_acesso == "USER"

def deny_if_not(condition: Any, message: Any="Sem permissão"):
    if not condition:
        return HttpResponseForbidden(message)
    return None
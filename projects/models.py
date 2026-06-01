from __future__ import annotations
from typing import Any

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator

# Este arquivo define a estrutura do banco de dados (tabelas).
# Cada classe aqui representa uma tabela no banco.
# Os atributos da classe são as colunas dessa tabela.
# O Django usa isso para criar e gerenciar o banco via migrations.

class Fabricantes(models.Model):
    id_fabricante = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nome

class TiposMotor(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.descricao

class Locais(models.Model):
    id_local = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nome

class UsuarioManager(BaseUserManager["Usuarios"]):

    def create_user(self, matricula: str, nome: str, password: str|None = None, **extra_fields: Any):

        if not matricula:
            raise ValueError("Matrícula obrigatória")

        user = self.model(matricula=matricula, nome=nome, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula: str, nome: str, password: str|None = None, **extra_fields: Any):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("nivel_acesso", Usuarios.NivelAcesso.ADMIN)

        return self.create_user(matricula, nome, password, **extra_fields)


class Usuarios(AbstractBaseUser, PermissionsMixin):

    class NivelAcesso(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        USER = "USER", "User"

    id_usuario = models.AutoField(primary_key=True)

    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)

    senha_temporaria = models.BooleanField(default=True)

    nivel_acesso = models.CharField(max_length=10, choices=NivelAcesso.choices, default=NivelAcesso.USER)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "matricula"
    REQUIRED_FIELDS = ["nome"]

    objects: UsuarioManager = UsuarioManager() # type: ignore

    def __str__(self):
        return f"{self.nome} ({self.matricula})"


class Motores(models.Model):
    id_motor = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=100)
    potencia = models.CharField(max_length=30)
    tensao = models.CharField(max_length=30)
    corrente = models.CharField(max_length=50)
    rpm = models.CharField(max_length=40)
    modo_fixacao = models.CharField(max_length=100)
    quantidade = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    id_fabricante = models.ForeignKey(Fabricantes, on_delete=models.CASCADE, db_column='id_fabricante')
    id_tipo = models.ForeignKey(TiposMotor, on_delete=models.CASCADE, db_column='id_tipo')
    id_local = models.ForeignKey(Locais, on_delete=models.CASCADE, db_column='id_local')

    def __str__(self) -> str:
        return self.modelo


class Inspecoes(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'PENDENTE'),
        ('EM ANDAMENTO', 'EM ANDAMENTO'),
        ('CONCLUÍDO', 'CONCLUÍDO')
    ]

    id_inspecao = models.AutoField(primary_key=True)
    id_motor = models.ForeignKey(Motores, on_delete=models.CASCADE, db_column='id_motor')
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, db_column='id_usuario', null=True, blank=True)
    data_inspecao = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDENTE')
    observacoes = models.TextField()
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.observacoes
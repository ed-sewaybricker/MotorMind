from __future__ import annotations
from typing import Any

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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

class UsuarioManager(BaseUserManager['Usuarios']):

    def create_user(self, matricula: str, nome: str, password: str|None = None, **extra_fields:Any) -> "Usuarios":

        if not matricula:
            raise ValueError('A matrícula é obrigatória')

        if not nome:
            raise ValueError('O nome é obrigatório')

        user = self.model(matricula=matricula, nome=nome, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, matricula: str, nome: str, password: str|None = None, **extra_fields:Any) -> "Usuarios":

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(matricula, nome, password, **extra_fields)
    
class Usuarios(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    username = None

    USERNAME_FIELD = 'matricula'

    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    def __str__(self):
        return f'{self.nome} ({self.matricula})'

class Motores(models.Model):
    id_motor = models.AutoField(primary_key=True)
    modelo = models.CharField(max_length=100)
    potencia = models.CharField(max_length=30)
    tensao = models.CharField(max_length=30)
    corrente = models.CharField(max_length=50)
    rpm = models.CharField(max_length=40)
    modo_fixacao = models.CharField(max_length=100)
    id_fabricante = models.ForeignKey(Fabricantes, models.DO_NOTHING, db_column='id_fabricante')
    id_tipo = models.ForeignKey(TiposMotor, models.DO_NOTHING, db_column='id_tipo')
    id_local = models.ForeignKey(Locais, models.DO_NOTHING, db_column='id_local')

    def __str__(self) -> str:
        return self.modelo

'''
    MODIFICAR id_usuario QUANDO FIZERMOS O LOGIN
'''
class Inspecoes(models.Model):
    id_inspecao = models.AutoField(primary_key=True)
    id_motor = models.ForeignKey(Motores, models.DO_NOTHING, db_column='id_motor')
    id_usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario', null=True, blank=True) 
    data_inspecao = models.DateField()
    observacoes = models.TextField()

    def __str__(self) -> str:
        return self.observacoes

'''
    MODIFICAR id_usuario QUANDO FIZERMOS O LOGIN
'''
class Manutencoes(models.Model):
    id_manutencao = models.AutoField(primary_key=True)
    id_motor = models.ForeignKey(Motores, models.DO_NOTHING, db_column='id_motor')
    id_usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='id_usuario', null=True, blank=True)
    tipo = models.CharField(max_length=50)
    data_manutencao = models.DateField()
    descricao = models.TextField()

    def __str__(self) -> str:
        return self.descricao
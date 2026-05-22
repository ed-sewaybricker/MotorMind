from django.db import models

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

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nome

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
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your models here.

#alevino

class Alevino(models.Model):
    especie = models.CharField(max_length=50, unique = True)

    def __str__(self):
        return self.especie
    
#tanques

class Tanque(models.Model): 
    id_tanque = models.CharField(max_length=50, unique= True)
    especie_alevino = models.ForeignKey(Alevino, on_delete=models.CASCADE, null=True, blank=True)
    quantidade_povoada = models.PositiveIntegerField()
    data_povoamento = models.DateField(null=True, blank=True)
    data_retirada = models.DateField(null= True, blank= True)
    quantidade_retirada = models.PositiveIntegerField(null=True, blank=True)
    previsao_retirada = models.DateField(null= True, blank= True)
    observacoes = models.TextField(blank=True)
    estado_ativo = models.BooleanField(default=True)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def estado(self):
        return "Povoado" if self.estado_ativo else "Despovoado"

    @property
    def taxa_sobrevivencia(self):
        if self.quantidade_retirada and self.quantidade_povoada:
            return (self.quantidade_retirada / self.quantidade_povoada) * 100
        return None
    
    def __str__(self):
        return self.id_tanque

class HistoricoTanque(models.Model):
    tanque = models.ForeignKey(Tanque, on_delete=models.CASCADE, related_name='historico_baixas')
    especie = models.CharField(max_length=50)
    quantidade_povoada = models.PositiveIntegerField()
    quantidade_despovoada = models.PositiveIntegerField(null=True, blank=True) 
    data_povoamento = models.DateField()
    previsao_retirada = models.DateField(null=True, blank=True)
    data_real_retirada = models.DateField()
    taxa_sobrevivencia = models.FloatField()
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Histórico - {self.tanque.id_tanque} ({self.data_real_retirada})"

    
# models.py
class RetiradaParcial(models.Model):
    tanque = models.ForeignKey(Tanque, on_delete=models.CASCADE, related_name='retiradas_parciais')
    quantidade = models.PositiveIntegerField(null= True, blank= True)
    data = models.DateField(null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    
#insumos

# models.py
from django.db import models

class Insumo(models.Model):
    nome_produto = models.CharField(max_length=100, unique= True)
    quantidade_produto = models.PositiveIntegerField()
    estoque_minimo = models.PositiveIntegerField()
    data_compra = models.DateField()
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome_produto

    @property
    def is_below_minimum(self):
        return self.quantidade_produto <= self.estoque_minimo
    

#notificacao

from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class Notificacao(models.Model):
    mensagem = models.TextField()
    tipo = models.CharField(max_length=20, choices=[('warning', 'Aviso'), ('danger', 'Crítico')])
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.mensagem

    
#perfil
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, blank=True, null=True)
    imagem = models.ImageField(upload_to='perfil/', default='perfil/default.png', blank=True)
    

    def __str__(self):
        return self.user.username
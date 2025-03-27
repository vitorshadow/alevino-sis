from django import forms
from .models import Tanque, Alevino, Insumo, Profile
from django.core.exceptions import ValidationError

forms.DateInput.input_type = 'date'
forms.DateInput.format = '%Y-%m-%d'
#formulário tanque

class TanqueForm(forms.ModelForm):
    class Meta:
        model = Tanque
        fields = [
            'id_tanque', 'especie_alevino',
            'quantidade_povoada', 'data_povoamento',
            #'data_retirada', #'quantidade_retirada',
            'previsao_retirada',
        ]
        widgets = {
            'data_povoamento': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'data_retirada': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
            'previsao_retirada': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d'),
        }
        labels = {
            'id_tanque': 'Nome do Tanque',
            'especie_alevino': 'Espécie de Alevino',
            'quantidade_povoada': 'Quantidade Povoada',
            'data_povoamento': 'Data de Povoamento',
            #'data_retirada': 'Data de Retirada',
            #'quantidade_retirada': 'Quantidade Retirada',
            'previsao_retirada' : 'Previsão de Retirada'
        }

    def clean_id_tanque(self):
        id_tanque = self.cleaned_data.get('id_tanque')
        if Tanque.objects.exclude(pk=self.instance.pk).filter(id_tanque=id_tanque).exists():
            raise ValidationError("Esse nome já foi cadastrado, escolha outro.")
        return id_tanque

#formulário alevino

class AlevinoForm(forms.ModelForm):
    class Meta:
        model = Alevino
        fields = ['especie',]
        labels = {
            'especie': 'Nome da Espécie',
        }

#formulário insumos

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nome_produto', 'quantidade_produto', 'estoque_minimo', 'data_compra']
        widgets = {
            'data_compra': forms.DateInput(attrs={'type': 'date'},format='%Y-%m-%d')
        }
        labels = {
            'nome_produto': 'Nome do Produto',
            'quantidade_produto': 'Quantidade',
            'estoque_minimo': 'Insira Estoque Mínimo',
            'data_compra': 'Data de Entrada'
        }

    def clean_nome_produto(self):
        nome_produto = self.cleaned_data.get('nome_produto')
        if Insumo.objects.exclude(pk=self.instance.pk).filter(nome_produto=nome_produto).exists():
            raise ValidationError("Esse nome já foi cadastrado, escolha outro.")
        return nome_produto
    
#formulario perfil
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nome', 'imagem']
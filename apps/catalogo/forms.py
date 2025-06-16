from django import forms
from django.forms import inlineformset_factory, modelformset_factory

from apps.catalogo.models import Item, ItemFabricante, Fabricante


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'nome_reduzido', 'descricao', 'ativo']
        labels = {
            'nome': 'Nome do Item',
            'nome_reduzido': 'Nome Reduzido',
            'descricao': 'Descricao',
            'ativo': 'Status',
        }

ItemFormSet = modelformset_factory(
    model=Item,
    form=ItemForm,
    extra=1,
    can_delete=True,
)


class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ['nome', 'nome_reduzido', 'ativo']
        labels = {
            'nome': 'Nome do Fabricante',
            'nome_reduzido': 'Nome Reduzido',
            'ativo': 'Status',
        }

FabricanteFormSet = modelformset_factory(
    model=Fabricante,
    form=FabricanteForm,
    extra=1,
    can_delete=True,
)

class ItemFabricanteForm(forms.ModelForm):
    class Meta:
        model = ItemFabricante
        fields = ['item', 'fabricante', 'tamanho_calcado', 'preco', 'imagem']
        labels = {
            'item': 'Item',
            'fabricante': 'Fabricante',
            'tamanho_calcado': 'Tamanho Calçado',
            'preco': 'Preço',
            'imagem': 'Imagem para o catálogo',
        }
        widgets = {
            'id': forms.HiddenInput(),
        }



ItemFabricanteFormSet = modelformset_factory(
    model=ItemFabricante,
    form=ItemFabricanteForm,
    extra=1,
    can_delete=True,
)
from django import forms
from django.forms import inlineformset_factory

from apps.catalogo.models import Item, ItemFabricante


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome', 'nome_reduzido', 'descricao', 'ativo']


class ItemFabricanteForm(forms.ModelForm):
    class Meta:
        model = ItemFabricante
        fields = ['fabricante', 'tamanho_calcado', 'preco']
        widgets = {
            'preco': forms.NumberInput(attrs={'step': '0.01'}),
        }

ItemFabricanteFormSet = inlineformset_factory(
    parent_model=Item,
    model=ItemFabricante,
    form=ItemFabricanteForm,
    extra=1,
    can_delete=True
)
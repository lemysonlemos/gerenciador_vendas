from django import forms
from django.forms import modelformset_factory

from apps.estoques.models import Estoque


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['qtd_estoque', 'catalogo', 'loja', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 2}),
        }

EstoqueFormSet = modelformset_factory(
    Estoque,
    form=EstoqueForm,
    extra=1,
    can_delete=True,
)
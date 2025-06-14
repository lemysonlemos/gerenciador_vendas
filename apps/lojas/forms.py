from django import forms
from django.forms import modelformset_factory

from apps.lojas.models import Loja


class LojaForm(forms.ModelForm):
    STATUS_CHOICES = (
        (True, 'Ativo'),
        (False, 'Inativo'),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(),
        label='Status'
    )
    class Meta:
        model = Loja
        fields = ['nome', 'descricao', 'status', 'justificativa']

    def clean_status(self):
        return self.cleaned_data['status'] == 'True'


LojaFormSet = modelformset_factory(
    Loja,
    form=LojaForm,
    extra=1,
    can_delete=False
)
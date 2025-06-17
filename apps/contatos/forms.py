import re
from django import forms
from django.forms.models import modelformset_factory

from apps.contatos.models import TipoContato, Contato


class ContatoForm(forms.ModelForm):
    tipo_contato = forms.ModelChoiceField(
        label='Tipo de Contato',
        queryset=TipoContato.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        required=True

    )
    contato = forms.CharField(
        label='Contato',
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        ),
        required=True
    )
    DELETE = forms.BooleanField(
        label='',
        required=False,
        widget=forms.HiddenInput
    )

    class Meta:
        model = Contato
        fields = ('tipo_contato', 'contato')


ContatoFormSet = modelformset_factory(
    Contato,
    form=ContatoForm,
    extra=1,
    min_num=0,
    max_num=3,
    validate_min=True,
    can_delete=True
)


from django import forms
from django_select2 import forms as s2forms

from apps.lojas.models import Loja
from apps.vinculos.models import Vinculo


class VinculoForm(forms.ModelForm):
    perfil = forms.ChoiceField(
        choices=Vinculo.STATUS_PERFIL,
        label='Perfil',
        widget=s2forms.Select2Widget(
            attrs={
                'class': 'form-control',
            }
        )
    )

    loja = forms.ModelChoiceField(
        queryset=Loja.objects.all().order_by('id'),
        label='Loja',
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Vinculo
        fields = ('perfil', 'loja')


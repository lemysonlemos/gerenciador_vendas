from django import forms
from django.forms import modelformset_factory
from django_select2 import forms as s2forms

from apps.enderecos.models import UnidadeFederativa, Municipio, TipoEndereco, Endereco


class EnderecoForm(forms.ModelForm):
    uf = forms.ModelChoiceField(
        queryset=UnidadeFederativa.objects.all().order_by('nome'),
        widget=s2forms.Select2Widget(
            attrs={
                'data-minimum-input-length': 2,
                'data-selection-css-class': 'form-control'
            }
        ),
    )

    municipio = forms.ModelChoiceField(
        label='Município',
        queryset=Municipio.objects.all(),
        widget=s2forms.Select2Widget(
            attrs={
                'data-minimum-input-length': 6,
                'data-selection-css-class': 'form-control'
            }
        ),
        required=True
    )
    rua = forms.CharField(
        label='Logradouro',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        required=True
    )
    numero = forms.CharField(
        label='Número',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        required=False
    )
    complemento = forms.CharField(
        label='Complemento',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        required=False
    )
    bairro = forms.CharField(
        label='Bairro',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        required=True
    )
    cep = forms.CharField(
        label='CEP',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '00000000'
            }
        ),
        max_length=8,
        required=True
    )
    tipo_endereco = forms.ModelChoiceField(
        label="Tipo",
        queryset=TipoEndereco.objects.all().exclude(id__in=[3, 4]),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
        required=True,
    )
    DELETE = forms.BooleanField(
        label='',
        required=False,
        widget=forms.HiddenInput
    )

    class Meta:
        model = Endereco
        fields = ('uf', 'municipio', 'rua', 'numero', 'complemento', 'bairro', 'cep', 'tipo_endereco')


EnderecoFormSet = modelformset_factory(
    Endereco,
    form=EnderecoForm,
    extra=0,
    min_num=1,
    max_num=3,
    validate_min=True,
    can_delete=True
)

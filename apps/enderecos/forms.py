from django import forms
from django.forms import modelformset_factory
from django_select2 import forms as s2forms

from apps.enderecos.models import UnidadeFederativa, Municipio, TipoEndereco, Endereco


class EnderecoForm(forms.ModelForm):
    uf = forms.ModelChoiceField(
        queryset=UnidadeFederativa.objects.filter(sigla='RN').order_by('nome'),
        widget=s2forms.Select2Widget(
            attrs={
                'data-minimum-input-length': 2,
                'data-selection-css-class': 'form-control'
            }
        ),
    )

    municipio = forms.ModelChoiceField(
        queryset=Municipio.objects.filter(uf__sigla='RN').order_by('nome'),
        widget=s2forms.Select2Widget(
            attrs={
                'data-minimum-input-length': 2,
                'data-selection-css-class': 'form-control'
            }
        ),
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

    def __init__(self, *args, **kwargs):
        self.visualizar = kwargs.pop('visualizar', None)
        self.uf_kw = kwargs.pop('uf', None)
        super().__init__(*args, **kwargs)

        if self.uf_kw:
            self.fields['uf'].queryset = UnidadeFederativa.objects.filter(
                sigla=self.uf_kw
            )
            self.fields['municipio'].queryset = Municipio.objects.filter(
                uf__sigla=self.uf_kw
            )

        if hasattr(self.instance, 'municipio'):
            self.fields['uf'].initial = Municipio.objects.get(id=self.instance.municipio.id).uf

        if self.visualizar:
            for field in self.fields:
                self.fields[field].widget.attrs["readonly"] = True
                self.fields[field].widget.attrs["disabled"] = True


EnderecoFormSet = modelformset_factory(
    Endereco,
    form=EnderecoForm,
    extra=0,
    min_num=1,
    max_num=3,
    validate_min=True,
    can_delete=True
)

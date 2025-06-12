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

    class Meta:
        model = Contato
        fields = ('tipo_contato', 'contato')

    def __init__(self, *args, **kwargs):
        self.visualizar = kwargs.pop('visualizar', None)
        super().__init__(*args, **kwargs)
        if self.visualizar:
            for field in self.fields:
                self.fields[field].widget.attrs["readonly"] = True
                self.fields[field].widget.attrs["disabled"] = True

    def clean(self):
        tipo_contato = self.cleaned_data.get('tipo_contato')
        contato = self.cleaned_data.get('contato')

        if tipo_contato and contato:
            if tipo_contato.expressao_validacao:
                regex = re.compile(tipo_contato.expressao_validacao)
                if not regex.match(contato):
                    self.add_error('contato', f'Verifique se o contato {contato} possui o formato '
                                              f'{tipo_contato.formato}.')

        return self.cleaned_data


ContatoFormSet = modelformset_factory(
    Contato,
    form=ContatoForm,
    extra=1,
    min_num=0,
    max_num=3,
    validate_min=True,
    can_delete=True
)

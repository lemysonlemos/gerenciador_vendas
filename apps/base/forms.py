from localflavor.br import forms as brforms
from django import forms


class BRCPFField(brforms.BRCPFField):
    default_error_messages = {
        'invalid': "Número de CPF inválido.",
        'max_digits': "Você deve digitar apenas os 11 números do CPF.",
    }
    widget = forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '___.___.__-__',
            'data-mask': '000.000.000-00',
        },
    )

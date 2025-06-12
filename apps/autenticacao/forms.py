import re
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django_select2 import forms as s2forms

from apps.base.forms import BRCPFField


class LoginForm(forms.Form):
    cpf = BRCPFField(
        max_length=14,
        min_length=14,
        label='CPF'
    )
    senha = forms.CharField(
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput
    )
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            api_params={'hl': 'pt-BR'}
        ),
        label='Verificação',
        help_text='Marque a caixa acima.',
        error_messages={
            'captcha_invalid': "Por favor, marque a caixa de verificação ao final do formulário.",
            'captcha_error': "Por favor, marque a caixa de verificação ao final do formulário."
        }
    )

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return ''.join(re.findall(r'\d+', cpf))
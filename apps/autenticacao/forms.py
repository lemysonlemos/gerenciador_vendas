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
        max_length=11,
        min_length=11,
        label='CPF'
    )
    senha = forms.CharField(
        min_length=6,
        max_length=20,
        widget=forms.PasswordInput
    )

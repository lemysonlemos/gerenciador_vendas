from django import forms
from datetime import datetime, date, timedelta
import re
from django.db.transaction import atomic
from django.utils.safestring import mark_safe
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django_select2 import forms as s2forms
from localflavor.br.forms import BRCPFField as BRCPFFormField

from apps.autenticacao.models import UsuarioBase
from apps.cliente.models import Cliente, AnexoCliente
from apps.enderecos.models import UnidadeFederativa, Pais, Municipio


class ClienteGestaoForm(forms.ModelForm):
    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        widget=forms.TextInput(
            attrs={
                'x-on:input': 'handleChangeCanImport',
                'placeholder': 'Ex: XXXXXXXXXXX'
            }
        ),
        required=False,
    )
    data_nascimento = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'max': date.today,
                'required': True,
            },
            format='%Y-%m-%d'
        ),
    )
    nome_mae = forms.CharField(
        label='Nome da Mãe',
        max_length=255,
        widget=forms.TextInput(attrs={
            'data-selection-css-class': 'form-control'
        }),
        required=True,
    )
    uf = forms.ModelChoiceField(
        label='Estado',
        queryset=UnidadeFederativa.objects.all().order_by('nome'),
        widget=s2forms.Select2Widget(
            attrs={
                'data-minimum-input-length': 2,
                'data-selection-css-class': 'form-control'
            }
        ),
        required=False,
    )
    pais_origem = forms.ModelChoiceField(
        label='País de origem',
        queryset=Pais.objects.all(),
        widget=s2forms.ModelSelect2Widget(
            model=Pais,
            search_fields=['nome__icontains', ],
            attrs={
                'data-minimum-input-length': 0,
                'data-selection-css-class': 'form-control'
            },
        ),
        required=True
    )
    naturalidade = forms.ModelChoiceField(
        label='Naturalidade',
        queryset=Municipio.objects.all(),
        widget=s2forms.HeavySelect2Widget(
            data_url='/enderecos/data-view/buscar-municipio/?as_dict=true',
            dependent_fields={'uf': 'uf'},
            attrs={
                'data-minimum-input-length': 1,
                'data-selection-css-class': 'form-control'
            },
        ),
        required=False
    )
    raca = forms.ChoiceField(
        label='Raça/Cor',
        choices=Cliente.RACA_CHOICES,
        widget=s2forms.Select2Widget(
            attrs={
                'data-minimum-input-length': 0,
                'data-selection-css-class': 'form-control'
            }
        ),
        required=True,
    )
    sexo = forms.ChoiceField(
        label='Sexo',
        choices=Cliente.SEXO_CHOICES,
        widget=s2forms.Select2Widget(
            attrs={
                'data-minimum-input-length': 0,
                'data-selection-css-class': 'form-control'
            }
        ),
        required=True,
    )
    profissao = forms.CharField(
        label='Profissão',
        max_length=255,
        widget=forms.TextInput(
                attrs={'type': 'text'},
            ),
        required=False,
    )


    class Meta:
        model = Cliente
        fields = [
            'cpf', 'passaporte', 'nome_completo', 'nome_social', 'pais_origem', 'uf', 'naturalidade', 'nome_mae',
            'sexo', 'raca', 'data_nascimento', 'profissao',
        ]

    def __init__(self, *args, tipo=None, **kwargs):
        self.visualizar = kwargs.pop('visualizar', None)
        self.eh_edicao = kwargs.pop('eh_edicao', False)
        super().__init__(*args, **kwargs)

        if 'naturalidade' in self.initial and self.initial['naturalidade']:
            naturalidade_id = self.initial['naturalidade']
            municipio = Municipio.objects.get(id=naturalidade_id)
            self.fields['uf'].initial = municipio.uf

        if self.visualizar:
            for field in self.fields:
                self.fields[field].widget.attrs["readonly"] = True
                self.fields[field].widget.attrs["disabled"] = True
        else:
            if self.instance:
                if self.instance.cpf:
                    self.fields['cpf'].widget.attrs["readonly"] = True

    def clean_nome_mae(self):
        nome_mae = self.cleaned_data.get('nome_mae')
        if len(nome_mae) < 5:
            raise forms.ValidationError("O nome da mãe é inválido.")
        return nome_mae

    def clean_data_nascimento(self):
        data_atual = datetime.now().date()
        data_minima = datetime(1900, 1, 1).date()
        data_nascimento = self.cleaned_data['data_nascimento']
        if data_nascimento > data_atual:
            raise forms.ValidationError("A data de nascimento não pode ser maior que a data atual.")
        if data_nascimento < data_minima:
            raise forms.ValidationError("A data de nascimento não é válida.")
        return data_nascimento

    def clean_naturalidade(self):
        pais_origem = self.cleaned_data['pais_origem']
        naturalidade = self.cleaned_data['naturalidade']

        if pais_origem.id == 29 and not naturalidade:
            raise forms.ValidationError("A naturalidade é obrigatória para cidadãos brasileiros.")
        return naturalidade

    def clean(self):
        cpf = self.cleaned_data.get('cpf')
        passaporte = self.cleaned_data.get('passaporte')
        if not cpf  and not passaporte:
            mensagem = "Informe ao menos um dos seguintes documentos: CPF ou Passaporte."
            self.add_error('cpf', mensagem)
            self.add_error('passaporte', mensagem)


class ClienteForm(ClienteGestaoForm):
    class Meta:
        model = Cliente
        fields = ClienteGestaoForm.Meta.fields + ['passaporte', 'foto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['cpf'].widget.attrs["readonly"] = True
            self.fields['nome_completo'].widget.attrs["readonly"] = True
            self.fields['nome_mae'].widget.attrs["readonly"] = True
            self.fields['data_nascimento'].widget.attrs["readonly"] = True
            self.fields['sexo'].widget.attrs["readonly"] = True


class AnexoClienteForm(forms.ModelForm):
    arquivo = forms.FileField(
        label='Documento',
        required=False
    )

    class Meta:
        model = AnexoCliente
        fields = ['arquivo']

    def __init__(self, *args, **kwargs):
        self.visualizar = kwargs.pop('visualizar', None)
        super().__init__(*args, **kwargs)

        if self.visualizar:
            for field in self.fields:
                self.fields[field].widget.attrs["readonly"] = True
                self.fields[field].widget.attrs["disabled"] = True

    def save(self, commit=True):
        if self.cleaned_data.get('arquivo'):
            instance = super().save(commit=False)

            if commit:
                instance.save()
            return instance
        return None


class CadastrarClienteForm(forms.ModelForm):
    cpf = forms.HiddenInput()
    senha = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=6,
        max_length=20,
        help_text='Sua senha deve ter entre 6 e 20 dígitos'
    )
    senha_confirmacao = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmação de senha',
        min_length=6,
        max_length=20
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
    data_nascimento = forms.DateField(
        label='Data de nascimento',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control input_bg',
                'max': date.today,
                'required': True,
                'min': datetime.now().date() - timedelta(days=130 * 365),
            }
        ),
        required=True,
    )
    uf = forms.ModelChoiceField(
        label='Estado',
        queryset=UnidadeFederativa.objects.all().order_by('nome'),
        widget=s2forms.Select2Widget(
            attrs={
                'data-minimum-input-length': 2,
                'data-selection-css-class': 'form-control'
            }
        ),
        required=False,
    )
    naturalidade = forms.ModelChoiceField(
        label='Naturalidade',
        queryset=Municipio.objects.all(),
        widget=s2forms.HeavySelect2Widget(
            data_url='/enderecos/data-view/buscar-municipio/?as_dict=true',
            dependent_fields={'uf': 'uf'},
            attrs={
                'data-minimum-input-length': 2,
                'data-selection-css-class': 'form-control'
            },
        ),
        required=True
    )
    field_order = [
        'nome_completo', 'nome_social', 'data_nascimento', 'uf', 'naturalidade', 'sexo', 'raca',
        'profissao', 'senha', 'senha_confirmacao',
    ]

    class Meta:
        model = Cliente
        fields = [
            'foto', 'nome_completo', 'nome_social', 'data_nascimento', 'uf', 'naturalidade',
            'sexo', 'raca',  'profissao',]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={
                'max': date.today,
                'min': date(1870, 1, 1),
                'required': True
            }),
            'naturalidade': s2forms.Select2Widget(
                attrs={
                    'data-minimum-input-length': 2,
                    'data-selection-css-class': 'form-control'
                }
            ),
            'profissao': forms.TextInput(),
        }

    def clean_senha_confirmacao(self):
        senha = self.cleaned_data.get("senha")
        senha_confirmacao = self.cleaned_data.get("senha_confirmacao")
        if senha != senha_confirmacao:
            raise forms.ValidationError(
                "A senha e a confirmação precisam ser iguais. Por favor, digite novamente."
            )
        return self.cleaned_data["senha_confirmacao"]


    @atomic
    def save(self):
        usuario = UsuarioBase(username=f'{self.instance.cpf}_cliente')
        usuario.set_password(self.cleaned_data['senha'])
        usuario.save()
        self.instance.user = usuario
        return super().save()



class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['foto', 'nome_completo', 'nome_social', 'data_nascimento', 'sexo', 'raca',
                  'passaporte', 'profissao',]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={
                'max': date.today,
                'min': date(1870, 1, 1),
                'required': True
            }),
            'profissao': forms.TextInput(),
        }

    def clean_cpf(self):
        val = self.cleaned_data.get('cpf').replace(".", "").replace("-", "")
        if not self.instance:
            if val and Cliente.objects.filter(cpf=val).exists():
                raise forms.ValidationError(
                    'Já existe um usuário cadastrado com esse CPF.')
        return val


    @atomic
    def save(self):
        self.instance.cpf = self.instance.cpf.replace(".", "").replace("-", "")
        usuario, criado = UsuarioBase.objects.get_or_create(username=f'{self.instance.cpf}_cliente')
        usuario.save()
        self.instance.user = usuario
        return super().save()


class CpfForm(forms.Form):
    cpf = BRCPFFormField(label='CPF')

    def clean_cpf(self):
        return re.sub(r'\D', '', self.cleaned_data['cpf'])
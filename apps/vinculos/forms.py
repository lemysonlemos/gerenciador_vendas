from django import forms

from apps.vinculos.models import Vinculo



class VinculoForm(forms.ModelForm):
    class Meta:
        model = Vinculo
        fields = ['usuario', 'loja', 'status', 'perfil']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'loja': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'perfil': forms.Select(attrs={'class': 'form-select'}),
        }


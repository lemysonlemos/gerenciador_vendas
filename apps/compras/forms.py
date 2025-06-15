from django import forms

from apps.compras.models import Compra


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['qtd_compra', 'pagamento']

    estoque_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        qtd = cleaned_data.get('qtd_compra')
        estoque_id = cleaned_data.get('estoque_id')

        if not estoque_id:
            raise forms.ValidationError("Estoque inválido.")

        from apps.estoques.models import Estoque
        try:
            estoque = Estoque.objects.get(id=estoque_id)
        except Estoque.DoesNotExist:
            raise forms.ValidationError("Estoque não encontrado.")

        if qtd is None or qtd <= 0:
            raise forms.ValidationError("Quantidade deve ser maior que zero.")

        if estoque.qtd_estoque < qtd:
            raise forms.ValidationError("Quantidade em estoque insuficiente.")

        # Salva o estoque no form para usar depois
        self.estoque_obj = estoque

        return cleaned_data


class CompraGestaoForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['cliente', 'qtd_compra', 'pagamento']

    estoque_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()
        qtd = cleaned_data.get('qtd_compra')
        estoque_id = cleaned_data.get('estoque_id')

        if not estoque_id:
            raise forms.ValidationError("Estoque inválido.")

        from apps.estoques.models import Estoque
        try:
            estoque = Estoque.objects.get(id=estoque_id)
        except Estoque.DoesNotExist:
            raise forms.ValidationError("Estoque não encontrado.")

        if qtd is None or qtd <= 0:
            raise forms.ValidationError("Quantidade deve ser maior que zero.")

        if estoque.qtd_estoque < qtd:
            raise forms.ValidationError("Quantidade em estoque insuficiente.")

        # Salva o estoque no form para usar depois
        self.estoque_obj = estoque

        return cleaned_data
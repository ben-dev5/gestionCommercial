from django import forms
from decimal import Decimal
from django.core.exceptions import ValidationError

class ProductForm(forms.Form):
    product_description = forms.CharField(
        label='Description',
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    price_ht = forms.DecimalField(
        label='Prix HT',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    tax = forms.DecimalField(
        label='Taxe (%)',
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    price_it = forms.DecimalField(
        label='Prix TTC',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
        required=False
    )
    product_type = forms.ChoiceField(
        label='Type de produit',
        choices=[
            ('achat', 'Achat chez fournisseur'),
            ('vente', 'Vente au client'),
            ('achat/vente', 'Achat et vente'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        price_ht = cleaned_data.get('price_ht')
        tax = cleaned_data.get('tax')

        if price_ht is not None and tax is not None:
            price_it_calculated = price_ht * (Decimal(1) + tax / Decimal(100))
            cleaned_data['price_it'] = price_it_calculated.quantize(Decimal('0.01'))
        else:
            raise ValidationError("Le prix HT et la taxe sont requis pour calculer le prix TTC.")

        return cleaned_data

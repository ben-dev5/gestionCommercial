from django import forms

from django.core.exceptions import ValidationError

class ProductForm(forms.Form):
    product_description = forms.CharField(
        label='Description',
        max_length=40,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    price_ht = forms.FloatField(
        label='Prix HT',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    tax = forms.FloatField(
        label='Taxe (%)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    price_it = forms.FloatField(
        label='Prix TTC',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
        disabled=True,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        price_ht = cleaned_data.get('price_ht')
        tax = cleaned_data.get('tax')

        if price_ht is not None and tax is not None:
            price_it_calculated = price_ht * (1 + tax / 100)
            cleaned_data['price_it'] = round(price_it_calculated, 2)
        else:
            raise ValidationError("Le prix HT et la taxe sont requis pour calculer le prix TTC.")

        return cleaned_data

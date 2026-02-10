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
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})

    )

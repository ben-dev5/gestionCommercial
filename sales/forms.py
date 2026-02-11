from django import forms
from decimal import Decimal
from django.core.exceptions import ValidationError


class SalesOrderForm(forms.Form):
    contact_id = forms.ChoiceField(
        label='Contact',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    genre = forms.CharField(
        label='Genre',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Prestation, Fourniture...'
        })
    )
    type = forms.ChoiceField(
        label='Type',
        choices=[
            ('Devis', 'Devis'),
            ('Commande', 'Commande'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, contacts=None, **kwargs):
        super().__init__(*args, **kwargs)
        if contacts:
            self.fields['contact_id'].choices = [
                ('', '-- Sélectionnez un contact --'),
            ] + [
                (str(contact.contact_id), f"{contact.first_name} {contact.last_name}")
                for contact in contacts
            ]
        else:
            self.fields['contact_id'].choices = []


class SalesOrderLineForm(forms.Form):
    product_id = forms.ChoiceField(
        label='Produit',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    quantity = forms.IntegerField(
        label='Quantité',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1'
        })
    )
    price_ht = forms.DecimalField(
        label='Prix HT',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    tax = forms.DecimalField(
        label='Taxe (%)',
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    price_it = forms.DecimalField(
        label='Prix TTC',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'readonly': 'readonly'
        }),
        required=False
    )
    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    genre = forms.CharField(
        label='Genre',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Service, Fourniture...'
        })
    )

    def __init__(self, *args, products=None, **kwargs):
        super().__init__(*args, **kwargs)
        if products:
            self.fields['product_id'].choices = [
                ('', '-- Sélectionnez un produit --'),
            ] + [
                (str(product.product_id), product.product_description)
                for product in products
            ]
        else:
            self.fields['product_id'].choices = []

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


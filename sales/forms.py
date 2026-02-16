from django import forms
from django.core.exceptions import ValidationError
from products.services.product_service import ProductService


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
    price_it = forms.DecimalField(
        label='Prix TTC',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            #'readonly': 'readonly'
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
        product_id = cleaned_data.get('product_id')
        quantity = cleaned_data.get('quantity')

        if product_id:
            try:
                product_service = ProductService()
                product = product_service.get_product_by_id(product_id)

                if product and quantity:
                    price_ht = product.price_ht
                    tax = product.tax
                    # Calcul du prix TTC unitaire, puis multiplication par la quantité
                    price_ht_total = price_ht * quantity
                    price_it_calculated = price_ht_total * (1 + tax / 100)
                    cleaned_data['price_it'] = price_it_calculated
                elif not quantity:
                    raise ValidationError("Veuillez entrer une quantité.")
                else:
                    raise ValidationError("Produit introuvable.")
            except ValidationError:
                raise
            except Exception as e:
                raise ValidationError(f"Erreur lors de la récupération du produit : {str(e)}")
        else:
            raise ValidationError("Veuillez sélectionner un produit.")

        return cleaned_data


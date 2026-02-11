from django import forms
from django.core.exceptions import ValidationError


def validate_siret(value):
    if not value.isdigit():
        raise ValidationError('Le SIRET doit contenir que des chiffres.')
    if len(value) != 14:
        raise ValidationError('Le SIRET doit avoir précisement 14 chiffres.')


class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le prénom'
        })
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le nom'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'exemple@email.com'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+33 6 12 34 56 78'
        })
    )
    type = forms.ChoiceField(
        required=True,
        choices=[
            ('', '-- Sélectionnez un type --'),
            ('client', 'Client'),
            ('fournisseur', 'Fournisseur'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    siret = forms.CharField(
        required=False,
        validators=[validate_siret],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '14 chiffres',
            'maxlength': '14',
            'pattern': '[0-9]{14}',
            'inputmode': 'numeric'
        })
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresse complète'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ville'
        })
    )
    state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Région'
        })
    )
    zip_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Code postal'
        })
    )


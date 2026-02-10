from django import forms
from django.core.exceptions import ValidationError
from commons.services.contact_service import ContactService

def validate_siret(value):
    if not value.isdigit():
        raise ValidationError('Le SIRET doit contenir que des chiffres.')
    if len(value) != 14:
        raise ValidationError('Le SIRET doit avoir précisement 14 chiffres.')


class ContactForm(forms.ModelForm):
    siret = forms.CharField(
        validators=[validate_siret],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '14 chiffres',
            'maxlength': '14',
            'pattern': '[0-9]{14}',
            'inputmode': 'numeric'
        })
    )

    class Meta:
        model = ContactService().get_contact_by_id(4)
        fields = ['first_name', 'last_name', 'email', 'phone', 'type', 'siret', 'address', 'city', 'state', 'zip_code']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemple@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+33 6 12 34 56 78'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', '-- Sélectionnez un type --'),
                ('client', 'Client'),
                ('fournisseur', 'Fournisseur'),
            ]),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse complète'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ville'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Région'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Code postal'
            }),
        }


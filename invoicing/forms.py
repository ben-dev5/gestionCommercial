from django import forms


class InvoiceStatusForm(forms.Form):
    status = forms.ChoiceField(
        label='Statut',
        choices=[
            ('En attente', 'En attente'),
            ('réglé', 'Réglé'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )


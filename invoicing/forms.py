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
class InvoiceDateForm(forms.Form):
    created_at = forms.DateTimeField(
        label='Date de création',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=False
    )

from django import forms



class InvoiceDateForm(forms.Form):
    created_at = forms.DateTimeField(
        label='Date de création',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        required=False
    )

from django.db import models

from invoicing.models.invoice_models import Invoice

METHOD_CHOICES = (
    ('Carte bancaire', 'Carte bancaire'),
    ('PayPal', 'PayPal'),
    ('Virement bancaire', 'Virement bancaire'),
    ('Chèque', 'Chèque'),
)

STATUS_CHOICES = (
    ('En attente', 'En attente'),
    ('En cours ', 'En cours'),
    ('Payé', 'Payé'),
)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    slug = models.SlugField(null=True)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='Carte bancaire')
    state_payment = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En attente')
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models

from invoicing.models.invoice_models import Invoice

METHOD_CHOICES = (
    ('Carte bancaire', 'Carte bancaire'),
    ('PayPal', 'PayPal'),
    ('Virement bancaire', 'Virement bancaire'),
    ('Chèque', 'Chèque'),
)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='Carte bancaire')
    status = models.ForeignKey(Invoice, on_delete=models.CASCADE)


from django.db import models

from commons.models.contact_models import Contact
from invoicing.models.invoice_models import Invoice
from products.models.product_models import Product



STATUS_CHOICE =  (
        ('En attente', 'En attente'),
        ('réglé', 'réglé'),
)


class InvoiceOrderLine(models.Model):
    invoice_order_line_id = models.AutoField(primary_key=True)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    price_ht = models.FloatField()
    tax = models.FloatField()
    price_tax = models.FloatField()
    quantity = models.IntegerField()
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='En attente' )
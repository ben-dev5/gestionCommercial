from django.db import models

from commons.models.contact_models import Contact


TYPE_CHOICES = (
    ('Devis', 'Devis'),
    ('Commande', 'Commande')
)
STATUS_CHOICES = (
    ('Envoyé', 'Envoyé'),
    ('Signé', 'Signé'),
    ('Commandé', 'Commandé'),
)

class SalesOrder(models.Model):
    sales_order_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    genre = models.CharField(max_length=30)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Devis')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    public_hash = models.CharField(max_length=64, unique=True, null=True, blank=True)
    public_hash_expires_at = models.DateTimeField(null=True, blank=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    signed_ip = models.GenericIPAddressField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Envoyé')
    class Meta:
        db_table = 'sales_order'

    def __str__(self):
        return f"{self.type} {self.sales_order_id} - {self.contact_id.first_name} {self.contact_id.last_name}"

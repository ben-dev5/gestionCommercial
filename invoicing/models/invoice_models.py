from django.db import models
from django.utils import timezone

from commons.models.contact_models import Contact


STATUS_CHOICES = (
    ('En attente', 'En attente'),
    ('réglé', 'Réglé'),
)


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30)
    siret = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    id_product = models.IntegerField()
    description_products = models.TextField()
    price_ht = models.IntegerField()
    tax = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En attente')
    # rendre la date non automatique pour pouvoir la renseigner lors de la création d'une facture à partir d'un devis
    created_at = models.DateTimeField(auto_now_add=False, null=False, default=timezone.now)


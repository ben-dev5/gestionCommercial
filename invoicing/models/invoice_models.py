from django.db import models

from commons.models.contact_models import Contact


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


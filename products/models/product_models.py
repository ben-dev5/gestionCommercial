from django.db import models

class Product(models.Model):

    PRODUCT_TYPE_CHOICES = (
        ('achat','achat'),
        ('vente','vente'),
        ('achat/vente','achat/vente')
    )

    product_id = models.AutoField(primary_key=True)
    product_description = models.TextField(max_length=40, unique=True)
    price_ht = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    price_it = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='achat/vente')
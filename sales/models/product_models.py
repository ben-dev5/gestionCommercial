from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_description = models.TextField()
    price_ht = models.FloatField()
    tax = models.FloatField()
    price_it = models.FloatField()
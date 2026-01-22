from django.db import models

from commons.models.contact_models import Contact


class SalesOrder(models.Model):
    sales_order_id = models.AutoField(primary_key=True)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    genre = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
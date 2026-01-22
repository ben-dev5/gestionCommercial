from django.db import models

from commons.models.contact_models import Contact
from sales.models.product_models import Product
from sales.models.sales_order_models import SalesOrder


class SalesOrderLine(models.Model):
    sales_order_line_id = models.AutoField(primary_key=True)
    sales_order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    price_ht = models.FloatField()
    tax = models.FloatField()
    quantity = models.IntegerField()
    date = models.DateField()
    genre = models.CharField(max_length=50)
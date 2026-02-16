from django.db import models

from commons.models.contact_models import Contact
from products.models.product_models import Product
from sales.models.sales_order_models import SalesOrder


class SalesOrderLine(models.Model):
    sales_order_line_id = models.AutoField(primary_key=True)
    sales_order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE)
    price_ht = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    price_it = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField()
    date = models.DateField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'sales_order_line'

    def __str__(self):
        return f"Ligne {self.sales_order_line_id} - {self.sales_order_id}"


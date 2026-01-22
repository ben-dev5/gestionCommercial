from django.contrib import admin

# Register your models here.
from .models import Product
from .models import SalesOrder
from .models import SalesOrderLine
admin.site.register(SalesOrderLine)
admin.site.register(SalesOrder)
admin.site.register(Product)


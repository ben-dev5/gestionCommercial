from django.contrib import admin

# Register your models here.
from .models import Invoice
from .models import InvoiceOrderLine

admin.site.register(Invoice)
admin.site.register(InvoiceOrderLine)



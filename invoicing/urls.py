from django.urls import path
from invoicing.views import InvoiceListView, InvoiceDetailView, CreateInvoiceFromSalesOrderView

app_name = 'invoicing'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('create-from-sales/<int:sales_order_pk>/', CreateInvoiceFromSalesOrderView.as_view(), name='create_from_sales'),
]


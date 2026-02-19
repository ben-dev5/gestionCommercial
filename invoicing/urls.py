from django.urls import path
from invoicing.views import InvoiceListView, InvoiceDetailView, CreateInvoiceFromSalesOrderView, InvoicePdfView, InvoiceDeleteView, InvoiceExportCSVView

app_name = 'invoicing'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),
    path('<int:pk>/pdf/', InvoicePdfView.as_view(), name='invoice_pdf'),
    path('<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice_delete'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('create-from-sales/<int:sales_order_pk>/', CreateInvoiceFromSalesOrderView.as_view(), name='create_from_sales'),
    path('invoices/export-csv/', InvoiceExportCSVView.as_view(), name='invoice_export_csv'),
]


from django.urls import path
from sales.views.views_sales_order import (
    SalesOrderListView,
    SalesOrderDetailView,
    SalesOrderCreateView,
    SalesOrderUpdateView,
    SalesOrderDeleteView)
from sales.views.views_sales_line import (
    SalesOrderLineCreateView,
    SalesOrderLineDeleteView,
    SalesOrderDownloadPDFView)


app_name = 'sales'

urlpatterns = [
    path('', SalesOrderListView.as_view(), name='sales_order_list'),
    path('type/<str:type>/', SalesOrderListView.as_view(), name='sales_order_list_by_type'),
    path('<int:pk>/', SalesOrderDetailView.as_view(), name='sales_order_detail'),
    path('<int:pk>/pdf/', SalesOrderDownloadPDFView.as_view(), name='sales_order_pdf'),
    path('create/', SalesOrderCreateView.as_view(), name='sales_order_create'),
    path('<int:pk>/update/', SalesOrderUpdateView.as_view(), name='sales_order_update'),
    path('<int:pk>/delete/', SalesOrderDeleteView.as_view(), name='sales_order_delete'),
    path('<int:sales_order_pk>/line/create/', SalesOrderLineCreateView.as_view(), name='sales_order_line_create'),
    path('<int:sales_order_pk>/line/<int:line_pk>/delete/', SalesOrderLineDeleteView.as_view(), name='sales_order_line_delete'),
]


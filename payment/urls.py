from django.urls import path
from payment.views import PaymentView, PaymentDeleteView, PaymentUpdateView

app_name = 'payment'

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
    path('<int:payment_id>/delete/', PaymentDeleteView.as_view(), name='payment_delete'),
    path('<int:payment_id>/update/', PaymentUpdateView.as_view(), name='payment_update'),
]


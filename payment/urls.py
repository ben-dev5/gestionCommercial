from django.urls import path
from payment.views import PaymentView

app_name = 'payment'

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
]

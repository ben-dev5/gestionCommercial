from django.shortcuts import render
from django.views.generic import TemplateView

from payment.services.payment_service import PaymentService


class PaymentView(TemplateView):
    template_name = 'payment/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_service = PaymentService()

        try:
            context['payment_service'] = payment_service.get_all_payments()
        except:
            context['payment_service'] = None

        return context
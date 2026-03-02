from payment.models import Payment
from invoicing.models.invoice_models import Invoice

class PaymentRepository:

    def create_payment(self, payment_method, state_payment, invoice_id, amount):
        # Récupérer l'instance Invoice
        try:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
        except Invoice.DoesNotExist:
            raise ValueError(f"La facture avec l'ID {invoice_id} n'existe pas")

        return Payment.objects.create(
            payment_method=payment_method,
            state_payment=state_payment,
            invoice_id=invoice,
            amount=amount
        )

    def get_payment_by_id(self, payment_id):
        return Payment.objects.get(payment_id=payment_id)

    def get_payments_by_invoice_id(self, invoice_id):
        return Payment.objects.filter(invoice_id=invoice_id).order_by('-created_at')

    def get_all_payments(self):
        return Payment.objects.all().order_by('payment_id')

    def update_payment(self, payment_id, payment_method, state_payment, invoice_id, amount):
        payment = Payment.objects.get(payment_id=payment_id)
        payment.payment_method = payment_method
        payment.state_payment = state_payment
        payment.invoice_id = invoice_id
        payment.amount = amount
        payment.save()
        return payment

    def delete_payment(self, payment_id):
        payment = Payment.objects.get(payment_id=payment_id)
        payment.delete()
        return True
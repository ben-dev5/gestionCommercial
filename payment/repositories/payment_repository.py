from payment.models import Payment

class PaymentRepository:

    def create_payment(self, payment_method, state_payment, invoice_id, amount):
        return Payment.objects.create(
            payment_method=payment_method,
            state_payment=state_payment,
            invoice_id=invoice_id,
            amount=amount
        )

    def get_payment_by_id(self, payment_id):
        return Payment.objects.get(payment_id=payment_id)

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
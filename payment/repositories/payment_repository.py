from payment.models import Payment
from invoicing.models.invoice_models import Invoice


class PaymentRepository:

    def create_payment(self, payment_method, state_payment, invoice_id, amount):
        # Récupérer l'instance Invoice et vérifier statut
        try:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            # Vérifier que la facture est au minimum "Confirmé" pour créer un paiement
            valid_statuses = ['Confirmé', 'Comptabilisé']
            if invoice.status not in valid_statuses:
                raise ValueError(f"Impossible de créer un paiement pour une facture avec le statut '{invoice.status}'. La facture doit être 'Confirmé' ou 'Comptabilisé' pour être payée.")
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

    # récupération status facture pour valider paiement
    def get_invoice_status(self, invoice_id):
        """Récupérer le statut d'une facture par son ID"""
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        return invoice.status

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

    def get_state_payment(self, payment_id):
        """Récupérer le statut d'un paiement par son ID"""
        payment = Payment.objects.get(payment_id=payment_id)
        return payment.state_payment

    def is_invoice_fully_paid(self, invoice_id):
        """Vérifier si une facture est complètement payée"""
        try:
            invoice = Invoice.objects.get(invoice_id=invoice_id)
            # Récupérer le total des paiements pour cette facture
            payments = Payment.objects.filter(invoice_id=invoice_id, state_payment='Réglé')
            total_paid = sum(payment.amount for payment in payments)

            # Comparer avec le total TTC de la facture (calculé via la property total_amount)
            return total_paid >= invoice.total_amount
        except Invoice.DoesNotExist:
            return False

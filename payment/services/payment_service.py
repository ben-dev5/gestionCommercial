from payment.repositories.payment_repository import PaymentRepository

class PaymentService:

    def __init__(self):
        self.repo = PaymentRepository()

    def create_payment(self, payment_method, state_payment, invoice_id, amount):
        return self.repo.create_payment(payment_method, state_payment, invoice_id, amount)

    def get_payment_by_id(self, payment_id):
        return self.repo.get_payment_by_id(payment_id)

    def get_payments_by_invoice_id(self, invoice_id):
        return self.repo.get_payments_by_invoice_id(invoice_id)

    def get_all_payments(self):
        return self.repo.get_all_payments()

    def get_invoice_status(self, invoice_id):
        """Récupérer le statut d'une facture par son ID"""
        return self.repo.get_invoice_status(invoice_id)

    def update_payment(self, payment_id, payment_method, state_payment, invoice_id, amount):
        return self.repo.update_payment(payment_id, payment_method, state_payment, invoice_id, amount)

    def delete_payment(self, payment_id):
        return self.repo.delete_payment(payment_id)

    def get_state_payment(self, payment_id):
        """Récupérer le statut d'un paiement par son ID"""
        return self.repo.get_state_payment(payment_id)

    def is_invoice_fully_paid(self, invoice_id):
        """Vérifier si une facture est complètement payée"""
        return self.repo.is_invoice_fully_paid(invoice_id)

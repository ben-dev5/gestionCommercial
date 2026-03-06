from django.contrib.messages.context_processors import messages
from django.template.loader import render_to_string
from payment.repositories.payment_repository import PaymentRepository

class PaymentService:

    def __init__(self):
        self.repo = PaymentRepository()

    def create_payment(self, payment_method, state_payment, invoice_id, amount):
        # Vérifier que facture n'est pas en statut "Brouillon" ou "Annulée" avant de créer un paiement
        if self.repo.get_invoice_status(invoice_id) in ['Brouillon', 'Annulée']:
            return {'success': False, 'error': "Impossible de créer un paiement pour une facture en statut 'Brouillon' ou 'Annulée'. Veuillez vérifier le statut de la facture avant de créer un paiement."}

        # Vérifier que le reste à payer est supérieur à 0 avant de créer un paiement
        if self.repo.get_state_invoice_payment(invoice_id):
            return {'success': False, 'error': "Impossible de créer un paiement pour une facture déjà payée. Veuillez vérifier le statut de la facture avant de créer un paiement."}

        return self.repo.create_payment(payment_method, state_payment, invoice_id, amount)

    def get_payment_by_id(self, payment_id):
        return self.repo.get_payment_by_id(payment_id)

    def get_payments_by_invoice_id(self, invoice_id):
        return self.repo.get_payments_by_invoice_id(invoice_id)

    def get_all_payments(self):
        return self.repo.get_all_payments()

    def get_invoice_payment_status(self, invoice_id):
        """
        Déterminer le statut de paiement réel d'une facture.
        Retourne:
        - 'Payé' si tous les paiements sont en statut 'Payé' ET le montant total est couvert
        - 'En attente' s'il y a des paiements en statut 'En attente'
        - 'En cours' s'il y a des paiements en statut 'En cours'
        - 'Non payé' si aucun paiement
        """
        payments = self.repo.get_payments_by_invoice_id(invoice_id)

        if not payments:
            return 'Non payé'

        # Vérifier si tous les paiements sont en statut 'Payé'
        payment_states = [p.state_payment for p in payments]

        # S'il y a des paiements en attente
        if 'En attente' in payment_states:
            return 'En attente'

        # S'il y a des paiements en cours
        if 'En cours ' in payment_states or 'En cours' in payment_states:
            return 'En cours'

        # Vérifier si la facture est complètement payée
        if self.repo.get_state_invoice_payment(invoice_id):
            return 'Payé'

        return 'Non payé'

    def get_invoice_status(self, invoice_id):
        """Récupérer le statut d'une facture par son ID"""

        # Ne comptabilise pas les paiements si les paiements sont en statut "En attente" ou "En cours"
        if self.repo.get_state_invoice_payment(invoice_id):
            return "Payé"

        return self.repo.get_invoice_status(invoice_id)

    def update_payment(self, payment_id, payment_method, state_payment, invoice_id, amount):
        return self.repo.update_payment(payment_id, payment_method, state_payment, invoice_id, amount)

    def delete_payment(self, payment_id):
        return self.repo.delete_payment(payment_id)

    def get_state_payment(self, payment_id):
        """Récupérer le statut d'un paiement par son ID"""
        return self.repo.get_state_payment(payment_id)

    def get_payment_id_by_invoice_id(self, invoice_id):
        """Récupérer l'ID d'un paiement par l'ID de la facture associée"""
        payments = self.repo.get_payments_by_invoice_id(invoice_id)
        if payments.exists():
            return payments.first().payment_id
        return None


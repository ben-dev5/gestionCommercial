from invoicing.repositories.invoice_order_line_repository import InvoiceOrderLineRepository
from invoicing.services.invoice_service import InvoiceService
from products.services.product_service import ProductService
from commons.services.contact_service import ContactService


class InvoiceOrderLineService:
    def __init__(self):
        self.repo = InvoiceOrderLineRepository()
        self.invoice_service = InvoiceService()
        self.product_service = ProductService()
        self.contact_service = ContactService()

    def validate_invoice_order_line_data(self, invoice_id, product_id, contact_id, price_ht, tax, quantity, date):
        """Valider les données de la ligne de facture"""
        # Vérifier que la facture existe
        try:
            self.invoice_service.get_invoice_by_id(invoice_id)
        except:
            raise ValueError("La facture n'existe pas")

        # Vérifier que le produit existe
        try:
            self.product_service.get_product_by_id(product_id)
        except:
            raise ValueError("Le produit n'existe pas")

        # Vérifier que le contact existe
        try:
            self.contact_service.get_contact_by_id(contact_id)
        except:
            raise ValueError("Le contact n'existe pas")

        # Vérifier que price_ht est positif
        if price_ht < 0:
            raise ValueError("price_ht doit être positif")

        # Vérifier que tax est entre 0 et 100
        if tax < 0 or tax > 100:
            raise ValueError("tax doit être entre 0 et 100")

        # Vérifier que quantity est positif
        if quantity <= 0:
            raise ValueError("La quantité doit être positive")

    def create_invoice_order_line(self, invoice_id, product_id, contact_id, price_ht, tax, price_tax, quantity, date, status='En attente'):
        """Créer une nouvelle ligne de facture"""
        self.validate_invoice_order_line_data(invoice_id, product_id, contact_id, price_ht, tax, quantity, date)

        # Récupérer les objets
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        product = self.product_service.get_product_by_id(product_id)
        contact = self.contact_service.get_contact_by_id(contact_id)

        return self.repo.create_invoice_order_line(invoice, product, contact, price_ht, tax, price_tax, quantity, date, status)

    def delete_invoice_order_line(self, line_id):
        """Supprimer une ligne de facture"""
        return self.repo.delete_invoice_order_line(line_id)

    def get_all_invoice_order_lines(self):
        """Récupérer toutes les lignes de facture"""
        return self.repo.get_all_invoice_order_lines()

    def get_invoice_order_line_by_id(self, line_id):
        """Récupérer une ligne de facture par ID"""
        return self.repo.get_invoice_order_line_by_id(line_id)

    def get_invoice_order_lines_by_invoice(self, invoice_id):
        """Récupérer les lignes de facture d'une facture"""
        return self.repo.get_invoice_order_lines_by_invoice(invoice_id)

    def update_invoice_order_line(self, line_id, invoice_id, product_id, contact_id, price_ht, tax, price_tax, quantity, date, status):
        """Mettre à jour une ligne de facture"""
        self.validate_invoice_order_line_data(invoice_id, product_id, contact_id, price_ht, tax, quantity, date)

        # Récupérer les objets
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        product = self.product_service.get_product_by_id(product_id)
        contact = self.contact_service.get_contact_by_id(contact_id)

        return self.repo.update_invoice_order_line(line_id, invoice, product, contact, price_ht, tax, price_tax, quantity, date, status)


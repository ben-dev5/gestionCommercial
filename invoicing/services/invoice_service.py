from invoicing.repositories.invoice_repository import InvoiceRepository
from commons.services.contact_service import ContactService


class InvoiceService:
    def __init__(self):
        self.repo = InvoiceRepository()
        self.contact_service = ContactService()

    def validate_invoice_data(self, contact_id, name, address, city, state, zip_code, siret, email, phone):
        """Valider les données de la facture"""
        # Vérifier que le contact existe
        try:
            self.contact_service.get_contact_by_id(contact_id)
        except:
            raise ValueError("Le contact n'existe pas")

        # Vérifier que le nom n'est pas vide
        if not name or name.strip() == "":
            raise ValueError("Le nom ne peut pas être vide")

        # Vérifier que l'adresse n'est pas vide
        if not address or address.strip() == "":
            raise ValueError("L'adresse ne peut pas être vide")

        # Vérifier que la ville n'est pas vide
        if not city or city.strip() == "":
            raise ValueError("La ville ne peut pas être vide")

        # Vérifier que le code postal n'est pas vide
        if not zip_code or zip_code.strip() == "":
            raise ValueError("Le code postal ne peut pas être vide")

    def create_invoice(self, contact_id, name, address, city, state, zip_code, siret, email, phone):
        """Créer une nouvelle facture"""
        self.validate_invoice_data(contact_id, name, address, city, state, zip_code, siret, email, phone)
        contact = self.contact_service.get_contact_by_id(contact_id)
        return self.repo.create_invoice(contact, name, address, city, state, zip_code, siret, email, phone)

    def delete_invoice(self, invoice_id):
        """Supprimer une facture"""
        return self.repo.delete_invoice(invoice_id)

    def get_all_invoices(self):
        """Récupérer toutes les factures"""
        return self.repo.get_all_invoices()

    def get_invoice_by_id(self, invoice_id):
        """Récupérer une facture par ID"""
        return self.repo.get_invoice_by_id(invoice_id)

    def get_invoices_by_contact(self, contact_id):
        """Récupérer les factures d'un contact"""
        return self.repo.get_invoices_by_contact(contact_id)

    def update_invoice(self, invoice_id, contact_id, name, address, city, state, zip_code, siret, email, phone):
        """Mettre à jour une facture"""
        self.validate_invoice_data(contact_id, name, address, city, state, zip_code, siret, email, phone)
        contact = self.contact_service.get_contact_by_id(contact_id)
        return self.repo.update_invoice(invoice_id, contact, name, address, city, state, zip_code, siret, email, phone)


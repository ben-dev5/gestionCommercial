from invoicing.models.invoice_models import Invoice
from django.utils import timezone


class InvoiceRepository:
    def __init__(self):
        pass

    def create_invoice(self, contact, name, address, city, state, zip_code, siret, email, phone, status='En attente', created_at=None):
        """Créer une nouvelle facture"""
        invoice = Invoice.objects.create(
            contact_id=contact,
            name=name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            siret=siret,
            email=email,
            phone=phone,
            id_product=0,
            description_products='',
            price_ht=0,
            tax=0,
            status=status,
            created_at=timezone.now()
        )
        return invoice

    def get_invoice_by_id(self, invoice_id):
        """Récupérer une facture par ID"""
        try:
            return Invoice.objects.get(invoice_id=invoice_id)
        except Invoice.DoesNotExist:
            raise ValueError(f"Facture avec l'ID {invoice_id} non trouvée")

    def get_all_invoices(self):
        """Récupérer toutes les factures"""
        return Invoice.objects.all()

    def get_invoices_by_contact(self, contact_id):
        """Récupérer les factures d'un contact"""
        return Invoice.objects.filter(contact_id=contact_id)

    def update_invoice(self, invoice_id, contact, name, address, city, state, zip_code, siret, email, phone, status, created_at=None):
        """Mettre à jour une facture"""
        invoice = self.get_invoice_by_id(invoice_id)
        invoice.contact_id = contact
        invoice.name = name
        invoice.address = address
        invoice.city = city
        invoice.state = state
        invoice.zip_code = zip_code
        invoice.siret = siret
        invoice.email = email
        invoice.phone = phone
        invoice.status = status
        if created_at is not None:
            invoice.created_at = created_at
        invoice.save()
        return invoice

    def delete_invoice(self, invoice_id):
        """Supprimer une facture"""
        invoice = self.get_invoice_by_id(invoice_id)
        invoice.delete()

    def get_invoices_by_contact_id(self, contact_id):
        """Récupérer les factures d'un contact"""
        return Invoice.objects.filter(contact_id=contact_id)


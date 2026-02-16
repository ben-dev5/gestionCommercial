from invoicing.models.invoice_order_line_models import InvoiceOrderLine


class InvoiceOrderLineRepository:
    def __init__(self):
        pass

    def create_invoice_order_line(self, invoice, product, contact, price_ht, tax, price_tax, quantity, date):
        """Créer une nouvelle ligne de facture"""
        line = InvoiceOrderLine.objects.create(
            invoice_id=invoice,
            product_id=product,
            contact_id=contact,
            price_ht=price_ht,
            tax=tax,
            price_tax=price_tax,
            quantity=quantity,
            date=date
        )
        return line

    def get_invoice_order_line_by_id(self, line_id):
        """Récupérer une ligne de facture par ID"""
        try:
            return InvoiceOrderLine.objects.get(invoice_order_line_id=line_id)
        except InvoiceOrderLine.DoesNotExist:
            raise ValueError(f"Ligne de facture avec l'ID {line_id} non trouvée")

    def get_all_invoice_order_lines(self):
        """Récupérer toutes les lignes de facture"""
        return InvoiceOrderLine.objects.all()

    def get_invoice_order_lines_by_invoice(self, invoice_id):
        """Récupérer les lignes de facture d'une facture"""
        return InvoiceOrderLine.objects.filter(invoice_id=invoice_id)

    def update_invoice_order_line(self, line_id, invoice, product, contact, price_ht, tax, price_tax, quantity, date):
        """Mettre à jour une ligne de facture"""
        line = self.get_invoice_order_line_by_id(line_id)
        line.invoice_id = invoice
        line.product_id = product
        line.contact_id = contact
        line.price_ht = price_ht
        line.tax = tax
        line.price_tax = price_tax
        line.quantity = quantity
        line.date = date
        line.save()
        return line

    def delete_invoice_order_line(self, line_id):
        """Supprimer une ligne de facture"""
        line = self.get_invoice_order_line_by_id(line_id)
        line.delete()

    def delete_invoice_order_lines_by_invoice(self, invoice_id):
        """Supprimer toutes les lignes de facture d'une facture"""
        InvoiceOrderLine.objects.filter(invoice_id=invoice_id).delete()


from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import Http404
from django.contrib import messages

from invoicing.services.invoice_service import InvoiceService
from invoicing.services.invoice_order_line_service import InvoiceOrderLineService
from sales.services.sales_order_service import SalesOrderService
from sales.services.sales_order_line_service import SalesOrderLineService


class InvoiceListView(TemplateView):
    """Vue pour lister les factures"""
    template_name = 'invoicing/invoice_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice_service = InvoiceService()

        try:
            context['invoices'] = invoice_service.get_all_invoices()
        except:
            context['invoices'] = []

        return context


class InvoiceDetailView(TemplateView):
    """Vue pour afficher les détails d'une facture"""
    template_name = 'invoicing/invoice_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        invoice_service = InvoiceService()
        invoice_line_service = InvoiceOrderLineService()

        try:
            invoice = invoice_service.get_invoice_by_id(pk)
            lines = invoice_line_service.get_invoice_order_lines_by_invoice(pk)

            # Ajouter le total HT calculé pour chaque ligne
            for line in lines:
                line.total_ht = line.price_ht * line.quantity

            context['invoice'] = invoice
            context['lines'] = lines
            context['has_lines'] = len(lines) > 0
        except:
            raise Http404("Facture non trouvée")

        return context


class CreateInvoiceFromSalesOrderView(TemplateView):
    """Vue pour transformer un devis/commande en facture"""

    def post(self, request, *args, **kwargs):
        sales_order_pk = self.kwargs.get('sales_order_pk')
        sales_order_service = SalesOrderService()
        sales_order_line_service = SalesOrderLineService()
        invoice_service = InvoiceService()
        invoice_line_service = InvoiceOrderLineService()

        try:
            # Récupérer le devis/commande
            sales_order = sales_order_service.get_sales_order_by_id(sales_order_pk)
            sales_lines = sales_order_line_service.get_sales_order_lines_by_order(sales_order_pk)

            # Vérifier qu'il y a au moins une ligne
            if not sales_lines:
                messages.error(request, "Impossible de créer une facture sans lignes.")
                return redirect('sales:sales_order_detail', pk=sales_order_pk)

            # Créer la facture avec les données du contact
            contact = sales_order.contact_id
            invoice = invoice_service.create_invoice(
                contact_id=contact.contact_id,
                name=f"{contact.first_name} {contact.last_name}",
                address=contact.address,
                city=contact.city,
                state=contact.state,
                zip_code=contact.zip_code,
                siret=contact.siret,
                email=contact.email,
                phone=contact.phone
            )

            # Copier les lignes du devis/commande vers la facture
            for sales_line in sales_lines:
                invoice_line_service.create_invoice_order_line(
                    invoice_id=invoice.invoice_id,
                    product_id=sales_line.product_id.product_id,
                    contact_id=sales_line.contact_id.contact_id,
                    price_ht=sales_line.price_ht,
                    tax=sales_line.tax,
                    price_tax=sales_line.price_it,
                    quantity=sales_line.quantity,
                    date=sales_line.date,
                    status='En attente'
                )

            messages.success(request, f"Facture créée avec succès ! Numéro : {invoice.invoice_id}")
            return redirect('invoicing:invoice_detail', pk=invoice.invoice_id)

        except ValueError as e:
            messages.error(request, f"Erreur : {str(e)}")
            return redirect('sales:sales_order_detail', pk=sales_order_pk)
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
            return redirect('sales:sales_order_detail', pk=sales_order_pk)

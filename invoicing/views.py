from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import Http404
from django.contrib import messages
from datetime import datetime

from invoicing.services.invoice_service import InvoiceService
from invoicing.services.invoice_order_line_service import InvoiceOrderLineService
from invoicing.forms import InvoiceStatusForm
from sales.services.sales_order_service import SalesOrderService
from sales.services.sales_order_line_service import SalesOrderLineService
from django.http import FileResponse
from sales.sales_order_pdf import SalesOrderPDFService

import csv
from django.http import HttpResponse


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
            context['status_form'] = InvoiceStatusForm(initial={'status': invoice.status})
        except:
            raise Http404("Facture non trouvée")

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        invoice_service = InvoiceService()

        try:
            invoice = invoice_service.get_invoice_by_id(pk)
            form = InvoiceStatusForm(request.POST)

            if form.is_valid():
                new_status = form.cleaned_data['status']
                invoice_service.update_invoice(
                    invoice_id=pk,
                    contact_id=invoice.contact_id.contact_id,
                    name=invoice.name,
                    address=invoice.address,
                    city=invoice.city,
                    state=invoice.state,
                    zip_code=invoice.zip_code,
                    siret=invoice.siret,
                    email=invoice.email,
                    phone=invoice.phone,
                    status=new_status
                )
                messages.success(request, f"Statut mis à jour : {new_status}")
            else:
                messages.error(request, "Erreur lors de la mise à jour du statut")

        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")

        return redirect('invoicing:invoice_detail', pk=pk)


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
                    date=sales_line.date
                )

            messages.success(request, f"Facture créée avec succès ! Numéro : {invoice.invoice_id}")
            return redirect('invoicing:invoice_detail', pk=invoice.invoice_id)

        except ValueError as e:
            messages.error(request, f"Erreur : {str(e)}")
            return redirect('sales:sales_order_detail', pk=sales_order_pk)
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
            return redirect('sales:sales_order_detail', pk=sales_order_pk)

class InvoicePdfView(TemplateView):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        invoice_service = InvoiceService()
        invoice_line_service = InvoiceOrderLineService()
        pdf_service = SalesOrderPDFService()

        try:
            invoice = invoice_service.get_invoice_by_id(pk)
            lines = invoice_line_service.get_invoice_order_lines_by_invoice(pk)

            # Créer un objet facture compatible avec le service PDF
            class InvoicePdfAdapter:
                def __init__(self, invoice):
                    self.contact_id = invoice.contact_id
                    self.type = "Facture"
                    self.genre = "Facture"
                    self.created_at = datetime.now()
                    self.invoice_id = invoice.invoice_id

            # Créer des adaptateurs pour les lignes
            class InvoiceLinePdfAdapter:
                def __init__(self, line):
                    self.product_id = line.product_id
                    self.genre = line.product_id.product_description  # Utiliser la description du produit comme genre
                    self.quantity = line.quantity
                    self.price_ht = line.price_ht
                    self.tax = line.tax
                    self.price_it = line.price_tax  # Mapper price_tax vers price_it

            invoice_adapter = InvoicePdfAdapter(invoice)
            adapted_lines = [InvoiceLinePdfAdapter(line) for line in lines]

            pdf_buffer = pdf_service.generate_pdf(invoice_adapter, adapted_lines)

            return FileResponse(
                pdf_buffer,
                as_attachment=True,
                filename=f"facture_{pk}.pdf"
            )
        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")
            return redirect('invoicing:invoice_detail', pk=pk)


class InvoiceDeleteView(TemplateView):
    """Vue pour confirmer et supprimer une facture"""
    template_name = 'invoicing/invoice_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        invoice_service = InvoiceService()

        try:
            invoice = invoice_service.get_invoice_by_id(pk)
            context['invoice'] = invoice
        except:
            raise Http404("Facture non trouvée")

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        invoice_service = InvoiceService()

        try:
            invoice = invoice_service.get_invoice_by_id(pk)
            invoice_id = invoice.invoice_id
            invoice_service.delete_invoice(invoice_id)
            messages.success(request, f"Facture #{invoice_id} supprimée avec succès !")
            return redirect('invoicing:invoice_list')
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression : {str(e)}")
            return redirect('invoicing:invoice_list')

class InvoiceExportCSVView(TemplateView):
    """Vue pour exporter la liste des factures en CSV"""
    template_name = 'invoicing/invoice_list.html'
    def get(self, request, *args, **kwargs):
        invoice_service = InvoiceService()
        invoice_line_service = InvoiceOrderLineService()

        try:
            invoices = invoice_service.get_all_invoices()

            # Créer la réponse HTTP avec le type CSV
            response = HttpResponse(content_type='text/csv; charset=UTF-8')
            response['Content-Disposition'] = 'attachment; filename="factures.csv"'

            # Créer le writer CSV
            writer = csv.writer(response)

            # Ajouter l'en-tête
            writer.writerow([
                'ID Facture',
                'Contact',
                'Adresse',
                'Ville',
                'Code Postal',
                'Email',
                'Téléphone',
                'Montant HT',
                'Montant TTC',
                'Statut',
                'Date'
            ])

            # Ajouter les données des factures
            for invoice in invoices:
                try:
                    lines = invoice_line_service.get_invoice_order_lines_by_invoice(invoice.invoice_id)

                    # Calculer les totaux
                    total_ht = sum(line.price_ht for line in lines)
                    total_ttc = sum(line.price_tax for line in lines)

                    contact_name = f"{invoice.contact_id.first_name} {invoice.contact_id.last_name}"

                    writer.writerow([
                        invoice.invoice_id,
                        contact_name,
                        invoice.address,
                        invoice.city,
                        invoice.zip_code,
                        invoice.email,
                        invoice.phone,
                        f"{total_ht:.2f}",
                        f"{total_ttc:.2f}",
                        invoice.status,
                        invoice.created_at.strftime('%d/%m/%Y') if hasattr(invoice, 'created_at') else 'N/A'
                    ])
                except:
                    pass

            return response

        except Exception as e:
            messages.error(request, f"Erreur lors de l'export : {str(e)}")
            return redirect('invoicing:invoice_list')
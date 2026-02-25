from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import Http404, FileResponse
from django.contrib import messages

from sales.services.sales_order_service import SalesOrderService
from sales.services.sales_order_line_service import SalesOrderLineService
from sales.sales_order_pdf import SalesOrderPDFService
from products.services.product_service import ProductService
from sales.forms import  SalesOrderLineForm


class SalesOrderLineCreateView(TemplateView):
    template_name = 'sales/sales_order_line_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sales_order_pk = self.kwargs.get('sales_order_pk')
        service = SalesOrderService()
        product_service = ProductService()

        try:
            sales_order = service.get_sales_order_by_id(sales_order_pk)
        except:
            raise Http404("Devis/Commande non trouvé(e)")

        # Récupérer les produits de type vente ou achat/vente
        all_products = product_service.get_all_products()
        available_products = [p for p in all_products if p.product_type in ['vente', 'achat/vente']]

        if self.request.method == 'GET':
            context['form'] = SalesOrderLineForm(products=available_products)

        context['sales_order'] = sales_order
        context['products'] = available_products
        return context

    def post(self, request, *args, **kwargs):
        sales_order_pk = self.kwargs.get('sales_order_pk')
        service = SalesOrderService()
        line_service = SalesOrderLineService()
        product_service = ProductService()

        try:
            sales_order = service.get_sales_order_by_id(sales_order_pk)
        except:
            raise Http404("Devis/Commande non trouvé(e)")

        all_products = product_service.get_all_products()
        available_products = [p for p in all_products if p.product_type in ['vente', 'achat/vente']]

        form = SalesOrderLineForm(request.POST, products=available_products)

        if form.is_valid():
            try:
                product_id = int(form.cleaned_data['product_id'])
                product = product_service.get_product_by_id(product_id)

                # Vérifier que le produit est de type vente ou achat/vente
                if product.product_type not in ['vente', 'achat/vente']:
                    form.add_error('product_id', "Ce produit ne peut pas être vendu")
                else:
                    line_service.create_sales_order_line(
                        sales_order_id=sales_order_pk,
                        product_id=product_id,
                        contact_id=sales_order.contact_id.contact_id,
                        price_ht=product.price_ht,
                        tax=product.tax,
                        price_it=form.cleaned_data['price_it'],
                        quantity=form.cleaned_data['quantity'],
                        date=form.cleaned_data['date'],
                        genre=form.cleaned_data['genre'] or product.product_description
                    )
                    messages.success(request, "Ligne ajoutée avec succès !")
                    return redirect('sales:sales_order_detail', pk=sales_order_pk)
            except ValueError as e:
                form.add_error(None, str(e))

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class SalesOrderLineDeleteView(TemplateView):
    template_name = 'sales/sales_order_line_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        line_pk = self.kwargs.get('line_pk')
        sales_order_pk = self.kwargs.get('sales_order_pk')
        line_service = SalesOrderLineService()

        try:
            context['line'] = line_service.get_sales_order_line_by_id(line_pk)
            context['sales_order_pk'] = sales_order_pk
        except:
            raise Http404("Ligne non trouvée")

        return context

    def post(self, request, *args, **kwargs):
        line_pk = self.kwargs.get('line_pk')
        sales_order_pk = self.kwargs.get('sales_order_pk')
        line_service = SalesOrderLineService()

        try:
            line_service.delete_sales_order_line(line_pk)
            messages.success(request, "Ligne supprimée avec succès !")
        except:
            messages.error(request, "Erreur lors de la suppression")

        return redirect('sales:sales_order_detail', pk=sales_order_pk)


class SalesOrderDownloadPDFView(TemplateView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        service = SalesOrderService()
        line_service = SalesOrderLineService()

        try:
            sales_order = service.get_sales_order_by_id(pk)
            lines = line_service.get_sales_order_lines_by_order(pk)
        except:
            raise Http404("Devis/Commande non trouvé(e)")

        # Générer le PDF
        pdf_service = SalesOrderPDFService()
        pdf_buffer = pdf_service.generate_pdf(sales_order, lines)

        # Déterminer le nom du fichier
        doc_type = "Devis" if sales_order.type == "Devis" else "Commande"
        filename = f"{doc_type}_{sales_order.contact_id.last_name}_{pk}.pdf"

        # Retourner le PDF en téléchargement
        response = FileResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response



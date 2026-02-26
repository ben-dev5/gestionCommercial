from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages

from products.services.product_service import ProductService
from products.forms import ProductForm
from sales.services.sales_order_line_service import SalesOrderLineService
from invoicing.services.invoice_order_line_service import InvoiceOrderLineService

class ProductListView(TemplateView):
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = ProductService()
        context['products'] = service.get_all_products()

        products = service.get_all_products()

        # méthode de recherche de produits par description
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            context['products'] = [
                product for product in products
                if search_query.lower() in product.product_description.lower()
            ]
        return context


class ProductDetailView(TemplateView):
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        service = ProductService()
        context['product'] = service.get_product_by_id(pk)
        return context


class ProductCreateView(TemplateView):
    template_name = 'products/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['form'] = ProductForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                service = ProductService()
                service.create_product(
                    product_id=None,
                    product_description=form.cleaned_data['product_description'],
                    price_ht=form.cleaned_data['price_ht'],
                    tax=form.cleaned_data['tax'],
                    price_it=form.cleaned_data['price_it'],
                    product_type=form.cleaned_data['product_type']
                )
                return redirect('products:product_list')
            except ValueError as e:
                form.add_error(None, str(e))

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class ProductUpdateView(TemplateView):
    template_name = 'products/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        service = ProductService()
        product = service.get_product_by_id(pk)

        if self.request.method == 'GET':
            form = ProductForm(initial={
                'product_description': product.product_description,
                'price_ht': product.price_ht,
                'tax': product.tax,
                'price_it': product.price_it,
                'product_type': product.product_type,
            })
            context['form'] = form

        context['product'] = product
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        form = ProductForm(request.POST)

        if form.is_valid():
            try:
                service = ProductService()
                service.update_product(
                    product_id=pk,
                    product_description=form.cleaned_data['product_description'],
                    price_ht=form.cleaned_data['price_ht'],
                    tax=form.cleaned_data['tax'],
                    price_it=form.cleaned_data['price_it'],
                    product_type=form.cleaned_data['product_type']
                )
                return redirect('products:product_list')
            except ValueError as e:
                form.add_error(None, str(e))

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class ProductDeleteView(TemplateView):
    template_name = 'products/product_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        service = ProductService()
        sales_line_service = SalesOrderLineService()
        invoice_line_service = InvoiceOrderLineService()

        product = service.get_product_by_id(pk)

        # Vérifier l'utilisation du produit
        all_sales_lines = sales_line_service.get_all_sales_order_lines()
        all_invoice_lines = invoice_line_service.get_all_invoice_order_lines()

        sales_lines_count = len([line for line in all_sales_lines if line.product_id.product_id == pk])
        invoice_lines_count = len([line for line in all_invoice_lines if line.product_id.product_id == pk])

        context['product'] = product
        context['is_used'] = sales_lines_count > 0 or invoice_lines_count > 0
        context['sales_lines_count'] = sales_lines_count
        context['invoice_lines_count'] = invoice_lines_count

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        service = ProductService()
        sales_line_service = SalesOrderLineService()
        invoice_line_service = InvoiceOrderLineService()

        product = service.get_product_by_id(pk)

        # Vérifier l'utilisation du produit
        all_sales_lines = sales_line_service.get_all_sales_order_lines()
        all_invoice_lines = invoice_line_service.get_all_invoice_order_lines()

        sales_lines_count = len([line for line in all_sales_lines if line.product_id.product_id == pk])
        invoice_lines_count = len([line for line in all_invoice_lines if line.product_id.product_id == pk])

        # Si le produit est utilisé, empêcher la suppression
        if sales_lines_count > 0 or invoice_lines_count > 0:
            error_messages = []
            if sales_lines_count > 0:
                error_messages.append(f"{sales_lines_count} ligne(s) de devis/commande")
            if invoice_lines_count > 0:
                error_messages.append(f"{invoice_lines_count} ligne(s) de facture")

            documents = " et ".join(error_messages)
            messages.error(
                request,
                f"Impossible de supprimer ce produit. Il est utilisé dans {documents}. "
                f"Veuillez d'abord supprimer les lignes associées."
            )
            return redirect('products:product_detail', pk=pk)

        service.delete_product(pk)
        messages.success(request, f"Produit '{product.product_description}' supprimé avec succès !")
        return redirect('products:product_list')

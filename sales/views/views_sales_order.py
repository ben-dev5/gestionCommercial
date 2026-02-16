from django.shortcuts import redirect
from django.template import context
from django.views.generic import TemplateView
from django.http import Http404, FileResponse
from django.contrib import messages

from sales.services.sales_order_service import SalesOrderService
from sales.services.sales_order_line_service import SalesOrderLineService
from sales.sales_order_pdf import SalesOrderPDFService
from commons.services.contact_service import ContactService
from products.services.product_service import ProductService
from sales.forms import SalesOrderForm, SalesOrderLineForm


class SalesOrderListView(TemplateView):
    template_name = 'sales/sales_order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = SalesOrderService()
        order_type = self.kwargs.get('type', None)

        if order_type:
            context['sales_orders'] = service.get_sales_orders_by_type(order_type)
            context['order_type'] = order_type
        else:
            context['sales_orders'] = service.get_all_sales_orders()
            context['order_type'] = 'Tous'

        return context


class SalesOrderDetailView(TemplateView):
    template_name = 'sales/sales_order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        service = SalesOrderService()
        line_service = SalesOrderLineService()

        try:
            sales_order = service.get_sales_order_by_id(pk)
            lines = line_service.get_sales_order_lines_by_order(pk)

            # Ajouter le total HT calculé pour chaque ligne
            for line in lines:
                line.total_ht = line.price_ht * line.quantity

            context['sales_order'] = sales_order
            context['lines'] = lines
            context['has_lines'] = len(lines) > 0
        except:
            raise Http404("Devis/Commande non trouvé(e)")

        return context


class SalesOrderCreateView(TemplateView):
    template_name = 'sales/sales_order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_service = ContactService()
        product_service = ProductService()
        contacts = contact_service.get_all_contacts()

        all_products = product_service.get_all_products()
        available_products = [p for p in all_products if p.product_type in ['vente', 'achat/vente']]

        if self.request.method == 'GET':
            context['form'] = SalesOrderForm(contacts=contacts)
            context['line_form'] = SalesOrderLineForm(products=available_products)
        context['contacts'] = contacts
        context['products'] = available_products
        return context

    def post(self, request, *args, **kwargs):
        contact_service = ContactService()
        contacts = contact_service.get_all_contacts()

        form = SalesOrderForm(request.POST, contacts=contacts)
        if form.is_valid():
            try:
                service = SalesOrderService()
                contact_id = int(form.cleaned_data['contact_id'])
                sales_order = service.create_sales_order(
                    contact_id=contact_id,
                    genre=form.cleaned_data['genre'],
                    order_type=form.cleaned_data['type']
                )
                messages.success(request, "Devis/Commande créé(e) avec succès !")
                return redirect('sales:sales_order_detail', pk=sales_order.sales_order_id)
            except ValueError as e:
                form.add_error(None, str(e))

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


class SalesOrderUpdateView(TemplateView):
    template_name = 'sales/sales_order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        service = SalesOrderService()
        contact_service = ContactService()

        try:
            sales_order = service.get_sales_order_by_id(pk)
        except:
            raise Http404("Devis/Commande non trouvé(e)")

        contacts = contact_service.get_all_contacts()

        if self.request.method == 'GET':
            form = SalesOrderForm(
                initial={
                    'contact_id': str(sales_order.contact_id.contact_id),
                    'genre': sales_order.genre,
                    'type': sales_order.type,
                },
                contacts=contacts
            )
            context['form'] = form

        context['contacts'] = contacts
        context['sales_order'] = sales_order
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        contact_service = ContactService()
        contacts = contact_service.get_all_contacts()

        form = SalesOrderForm(request.POST, contacts=contacts)

        if form.is_valid():
            try:
                service = SalesOrderService()
                contact_id = int(form.cleaned_data['contact_id'])
                service.update_sales_order(
                    sales_order_id=pk,
                    contact_id=contact_id,
                    genre=form.cleaned_data['genre'],
                    order_type=form.cleaned_data['type']
                )
                messages.success(request, "Devis/Commande modifié(e) avec succès !")
                return redirect('sales:sales_order_list')
            except ValueError as e:
                form.add_error(None, str(e))

        return self.render_to_response(context)


class SalesOrderDeleteView(TemplateView):
    template_name = 'sales/sales_order_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        service = SalesOrderService()

        try:
            context['sales_order'] = service.get_sales_order_by_id(pk)
        except:
            raise Http404("Devis/Commande non trouvé(e)")

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        service = SalesOrderService()
        service.delete_sales_order(pk)
        messages.success(request, "Devis/Commande supprimé(e) avec succès !")
        return redirect('sales:sales_order_list')



from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.http import Http404
from django.contrib import messages

from sales.services.sales_order_service import SalesOrderService
from sales.services.sales_order_line_service import SalesOrderLineService
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
        public_hash = self.request.GET.get('hash', None)
        service = SalesOrderService()
        line_service = SalesOrderLineService()

        try:
            sales_order = service.get_sales_order_by_id(pk)

            # Par défaut accès admin
            context['is_public_access'] = False

            # Si un hash est fourni en query string
            if public_hash:
                # Vérifier que le hash correspond ET qu'il est valide
                if service.get_public_hash(sales_order) == public_hash and service.is_hash_valid(sales_order):
                    context['is_public_access'] = True
                    # Sinon, on affiche juste un accès admin normal, pas d'erreur

            # Afficher le lien public temporairement s'il vient d'être généré
            if 'show_public_link' in self.request.session:
                if service.has_public_hash(sales_order):
                    public_hash_value = service.get_public_hash(sales_order)
                    context['public_link'] = service.build_public_url(self.request, sales_order.sales_order_id, public_hash_value)
                    context['show_public_link'] = True
                del self.request.session['show_public_link']

            lines = line_service.get_sales_order_lines_by_order(sales_order.sales_order_id)
            for line in lines:
                line.total_ht = line.price_ht * line.quantity

            context['sales_order'] = sales_order
            context['lines'] = lines
            context['has_lines'] = len(lines) > 0
        except ValueError as e:
            raise Http404(str(e))
        except Exception as e:
            raise Http404("Devis/Commande non trouvé(e)")

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        pk = self.kwargs.get('pk')
        public_hash = request.GET.get('hash', None)
        service = SalesOrderService()

        try:
            sales_order = service.get_sales_order_by_id(pk)

            # Vérifier si c'est un accès public
            is_public = (public_hash and service.get_public_hash(sales_order) == public_hash and service.is_hash_valid(sales_order))

            # Si accès public, seule la signature est autorisée
            if is_public:
                if action == 'sign':
                    client_ip = self._get_client_ip(request)
                    service.sign_sales_order(sales_order, client_ip=client_ip)
                    messages.success(request, "Devis/Commande signé(e) avec succès !")
                    return redirect(f'{request.path}?hash={public_hash}')
                else:
                    raise ValueError("Vous n'avez pas la permission d'effectuer cette action")

            # Génération du lien public (admin seulement)
            if action == 'generate_link':
                service.generate_public_hash(sales_order)
                request.session['show_public_link'] = True
                messages.success(request, "Lien public généré avec succès !")
                return redirect('sales:sales_order_detail', pk=pk)

            # Signature du devis (admin avec hash)
            elif action == 'sign' and public_hash:
                if not service.is_hash_valid(sales_order) or service.get_public_hash(sales_order) != public_hash:
                    raise ValueError("Lien d'accès invalide ou expiré")

                client_ip = self._get_client_ip(request)
                service.sign_sales_order(sales_order, client_ip=client_ip)
                messages.success(request, "Devis/Commande signé(e) avec succès !")
                return redirect(f'{request.path}?hash={public_hash}')

        except ValueError as e:
            messages.error(request, str(e))

        return self.get(request, *args, **kwargs)

    @staticmethod
    def _get_client_ip(request):
        """Récupère l'adresse IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


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

        context = self.get_context_data(**kwargs)
        context['form'] = form
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



class SalesOrderSignConfirmationView(TemplateView):
    template_name = 'sales/sales_order_sign_confirmation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        service = SalesOrderService()

        try:
            sales_order = service.get_sales_order_by_id(pk)
            context['sales_order'] = sales_order
        except:
            raise Http404("Devis/Commande non trouvé(e)")

        return context




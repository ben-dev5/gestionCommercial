from django.shortcuts import redirect
from django.views.generic import TemplateView

from products.services.product_service import ProductService
from django import forms
from products.forms import ProductForm

class ProductListView(TemplateView):
    template_name = 'products/product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = ProductService()
        context['products'] = service.get_all_products()
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
                    price_it=form.cleaned_data['price_it']
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
                    price_it=form.cleaned_data['price_it']
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
        context['product'] = service.get_product_by_id(pk)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        service = ProductService()
        service.delete_product(pk)
        return redirect('products:product_list')

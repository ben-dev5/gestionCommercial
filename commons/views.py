from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import Http404

from commons.services.contact_service import ContactService
from commons.forms import ContactForm


class ContactListView(TemplateView):
    template_name = 'commons/contact_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = ContactService()

        contacts = service.get_all_contacts()

        # recherche
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            contacts = [
                contact for contact in contacts
                if search_query.lower() in contact.first_name.lower()
                or search_query.lower() in contact.last_name.lower()
                or search_query.lower() in contact.email.lower()
            ]

        context['contacts'] = contacts
        return context


class ContactDetailView(TemplateView):
    template_name = 'commons/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = ContactService()
        try:
            contact = service.get_contact_by_id(self.kwargs['pk'])
            context['contact'] = contact
        except:
            raise Http404("Contact non trouvé")
        return context


class ContactCreateView(TemplateView):
    template_name = 'commons/contact_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = ContactForm(self.request.POST)
        else:
            context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            service = ContactService()
            contact = service.create_contact(
                contact_id=None,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                type=form.cleaned_data['type'],
                siret=form.cleaned_data['siret'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code'],
            )
            messages.success(request, f"Contact {contact.first_name} {contact.last_name} créé avec succès !")
            return redirect('commons:contact_list')
        return self.render_to_response(self.get_context_data())


class ContactUpdateView(TemplateView):
    template_name = 'commons/contact_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = ContactService()
        try:
            contact = service.get_contact_by_id(self.kwargs['pk'])
            context['object'] = contact
            if self.request.POST:
                context['form'] = ContactForm(self.request.POST, instance=contact)
            else:
                context['form'] = ContactForm(instance=contact)
        except:
            raise Http404("Contact non trouvé")
        return context

    def post(self, request, *args, **kwargs):
        service = ContactService()
        try:
            contact = service.get_contact_by_id(self.kwargs['pk'])
        except:
            raise Http404("Contact non trouvé")

        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            updated_contact = service.update_contact(
                contact_id=contact.contact_id,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                type=form.cleaned_data['type'],
                siret=form.cleaned_data['siret'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip_code=form.cleaned_data['zip_code'],
            )
            messages.success(request, f"Contact {updated_contact.first_name} {updated_contact.last_name} modifié avec succès !")
            return redirect('commons:contact_list')
        return self.render_to_response(self.get_context_data())


class ContactDeleteView(TemplateView):
    template_name = 'commons/contact_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = ContactService()
        try:
            contact = service.get_contact_by_id(self.kwargs['pk'])
            context['object'] = contact
        except:
            raise Http404("Contact non trouvé")
        return context

    def post(self, request, *args, **kwargs):
        service = ContactService()
        try:
            contact = service.get_contact_by_id(self.kwargs['pk'])
        except:
            raise Http404("Contact non trouvé")

        first_name = contact.first_name
        last_name = contact.last_name
        service.delete_contact(contact.contact_id)
        messages.success(request, f"Contact {first_name} {last_name} supprimé avec succès !")
        return redirect('commons:contact_list')

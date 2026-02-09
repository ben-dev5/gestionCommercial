from django.test import TestCase, Client
from django.urls import reverse
from commons.models import Contact
from commons.services.contact_service import ContactService


class ContactViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.service = ContactService()
        self.contact = self.service.create_contact(
            contact_id=1,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="+1 555 555 555",
            type="client",
            siret="12345678901234",
            address="123 Main St",
            city="Paris",
            state="IDF",
            zip_code="75000",
        )

    def test_contact_list_view(self):
        # Test accès à la liste des contacts
        response = self.client.get(reverse('commons:contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commons/contact_list.html')
        self.assertIn(self.contact, response.context['contacts'])

    def test_contact_detail_view(self):
        # Test accès au détail d'un contact
        response = self.client.get(reverse('commons:contact_detail', args=[self.contact.contact_id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commons/contact_detail.html')
        self.assertEqual(response.context['contact'], self.contact)

    def test_contact_create_view_get(self):
        # Test affichage du formulaire de création
        response = self.client.get(reverse('commons:contact_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'commons/contact_form.html')

    def test_contact_create_view_post(self):
        # Test création d'un contact avec formulaire
        data = {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com',
            'phone': '+1 555 123 456',
            'type': 'fournisseur',
            'siret': '98765432109876',
            'address': '456 Oak Ave',
            'city': 'Lyon',
            'state': 'RA',
            'zip_code': '69000',
        }
        response = self.client.post(reverse('commons:contact_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertEqual(Contact.objects.count(), 2)

    def test_contact_update_view(self):
        # Test modif d'un contact
        data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@example.com',
            'phone': '+1 555 555 555',
            'type': 'client',
            'siret': '12345678901234',
            'address': '123 Main St',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        response = self.client.post(reverse('commons:contact_update', args=[self.contact.contact_id]), data)
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.first_name, 'Jane')

    def test_contact_delete_view(self):
        # Test suppr d'un contact
        response = self.client.post(reverse('commons:contact_delete', args=[self.contact.contact_id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 0)

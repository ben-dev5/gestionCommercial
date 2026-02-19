from django.test import TestCase
from django.core.exceptions import ValidationError
from commons.forms import ContactForm, validate_siret


class ContactFormValidationTests(TestCase):

    def test_valid_contact_form(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '12345678901234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    # Tests SIRET - Longueur
    def test_siret_too_short(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '123456789012',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('siret', form.errors)
        self.assertIn('14 chiffres', str(form.errors['siret'][0]))

    def test_siret_too_long(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '123456789012345',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('siret', form.errors)

    # Tests SIRET - Caractères
    def test_siret_with_letters(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '1234567890123A',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('siret', form.errors)
        self.assertIn('chiffres', str(form.errors['siret'][0]))

    def test_siret_with_special_characters(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '12345678-90-1234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('siret', form.errors)

    def test_siret_with_spaces(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '1234 5678 9012 34',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('siret', form.errors)

    def test_siret_empty(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    # Tests Email
    def test_invalid_email(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'email_invalide',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '12345678901234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_valid_email(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '12345678901234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    # Tests Champs obligatoires
    def test_missing_first_name(self):
        data = {
            'first_name': '',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '12345678901234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)

    def test_missing_last_name(self):
        data = {
            'first_name': 'Jean',
            'last_name': '',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '12345678901234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors)

    def test_missing_type(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': '',  # Vide
            'siret': '12345678901234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('type', form.errors)

    # Tests Type de contact
    def test_valid_type_client(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'client',
            'siret': '12345678901234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_type_fournisseur(self):
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean@example.com',
            'phone': '+33 6 12 34 56 78',
            'type': 'fournisseur',
            'siret': '12345678901234',
            'address': '123 Rue de Paris',
            'city': 'Paris',
            'state': 'IDF',
            'zip_code': '75000',
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())

    def test_validate_siret_function_valid(self):
        try:
            validate_siret('12345678901234')
        except ValidationError:
            self.fail("validate_siret() a levé une ValidationError avec un SIRET valide")

    def test_validate_siret_function_invalid_length(self):
        with self.assertRaises(ValidationError):
            validate_siret('123456789012')

    def test_validate_siret_function_invalid_characters(self):
        with self.assertRaises(ValidationError):
            validate_siret('1234567890123A')


from django.test import TestCase
from commons.services.contact_service import ContactService
from commons.models import Contact

class ContactValidateFieldsTests(TestCase):
    def setUp(self):
        self.contact = Contact.services.create_contact(
            contact_id = "2",
            first_name="John",
            last_name="Doe",
            email="",
            phone="+1 555 555 555",
            type = "client",
            siret = "private",
            adress = "4 bakers street",
            city = "San Francisco",
            state = "CA",
            zip_code = "9410",
        )
    def test_validate_contact_field(self):
        # test que les champs ne sont pas vide
        self.assertIsNotNone(self.contact.last_name)
        self.assertIsNotNone(self.contact.first_name)
        self.assertIsNotNone(self.contact.email)
        self.assertIsNotNone(self.contact.phone)
        self.assertIsNotNone(self.contact.type)
        self.assertIsNotNone(self.contact.siret)
        self.assertIsNotNone(self.contact.adress)
        self.assertIsNotNone(self.contact.city)
        self.assertIsNotNone(self.contact.state)
        self.assertIsNotNone(self.contact.zip_code)
        self.assertIsNotNone(self.contact.contact_id)

        # test que les champs sont bien correpondants
        self.assertEqual(self.contact.last_name, "Doe")
        self.assertEqual(self.contact.first_name, "john")
        self.assertEqual(self.contact.email, "")
        self.assertEqual(self.contact.phone, "+1 555 555 555")
        self.assertEqual(self.contact.type, "client")
        self.assertEqual(self.contact.siret, "private")
        self.assertEqual(self.contact.adress, "4 bakers street")
        self.assertEqual(self.contact.city, "San Francisco")
        self.assertEqual(self.contact.state, "CA")
        self.assertEqual(self.contact.zip_code, "9410")
        self.assertEqual(self.contact.contact_id, "2")
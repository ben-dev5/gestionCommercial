from django.test import TestCase
from commons.services.contact_service import ContactService
from commons.models import Contact

class ContactValidateFieldsTests(TestCase):
    def setUp(self):
        self.service = ContactService()
        self.contact = self.service.create_contact(
            contact_id = "2",
            first_name="john",
            last_name="Doe",
            email="",
            phone="+1 555 555 555",
            type = "client",
            siret = "private",
            address = "4 bakers street",
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
        self.assertIsNotNone(self.contact.address)
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
        self.assertEqual(self.contact.address, "4 bakers street")
        self.assertEqual(self.contact.city, "San Francisco")
        self.assertEqual(self.contact.state, "CA")
        self.assertEqual(self.contact.zip_code, "9410")
        self.assertEqual(self.contact.contact_id, "2")

    def test_type_contact_field(self):
        # Créer un contact client
        self.service = ContactService()
        contact_client = self.service.create_contact(
            contact_id="3",
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            phone="+1 555 123 456",
            type="client",
            siret="12345678901234",
            address="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001",
        )

        # Créer un contact fournisseur
        self.service = ContactService()
        contact_fournisseur = self.service.create_contact(
            contact_id="4",
            first_name="Bob",
            last_name="Johnson",
            email="bob@example.com",
            phone="+1 555 789 012",
            type="fournisseur",
            siret="98765432109876",
            address="456 Oak Ave",
            city="Los Angeles",
            state="CA",
            zip_code="90001",
        )

        # Vérifier que les types sont différents
        self.assertNotEqual(contact_client.type, contact_fournisseur.type)
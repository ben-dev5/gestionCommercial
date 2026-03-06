from django.test import TestCase
from payment.services.payment_service import PaymentService
from commons.dtos import CreateContactDTO
from invoicing.services.invoice_service import InvoiceService
from payment.services.payment_service import PaymentService
from commons.services.contact_service import ContactService


# Create your tests here.
class PaymentTests(TestCase):
    def setUp(self):

        #Création d'un contact pour les tests
        self.contact_service = ContactService()
        contact_dto = CreateContactDTO (
            first_name="john",
            last_name="Doe",
            email="john@gmail.com",
            phone="+1 555 555 555",
            type = "client",
            siret = "private",
            address = "4 bakers street",
            city = "San Francisco",
            state = "CA",
            zip_code = "9410",
        )
        self.contact = self.contact_service.create_contact(contact_dto)

        # Création d'une facture pour les tests en récupérant les infos du contact
        self.invoice_service = InvoiceService()
        self.invoice = self.invoice_service.create_invoice(
            contact_id=self.contact.contact_id,
            name="Facture 001",
            address=self.contact.address,
            city=self.contact.city,
            state=self.contact.state,
            zip_code=self.contact.zip_code,
            siret=self.contact.siret,
            email=self.contact.email,
            phone=self.contact.phone,
            status="Confirmé"
        )

        # Création d'un paiement pour les tests
        self.service = PaymentService()
        payment = self.service.create_payment(
            payment_method="Carte bancaire",
            state_payment="En attente",
            invoice_id=self.invoice.invoice_id,
            amount=100
        )
        self.payment = payment


    def test_create_payment(self):
        # Récupérer le paiement créé via le service
        payment = self.service.get_payment_by_id(self.payment.payment_id)

        self.assertIsNotNone(payment)
        self.assertEqual(payment.payment_method, "Carte bancaire")
        self.assertEqual(payment.state_payment, "En attente")
        self.assertEqual(payment.invoice_id.invoice_id, self.invoice.invoice_id)
        self.assertEqual(payment.amount, 100)

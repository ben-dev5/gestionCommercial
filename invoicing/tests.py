from django.test import TestCase
from datetime import date


from invoicing.services.invoice_service import InvoiceService
from invoicing.services.invoice_order_line_service import InvoiceOrderLineService
from commons.services.contact_service import ContactService
from products.services.product_service import ProductService


class InvoiceTest(TestCase):

    def setUp(self):
        """Initialiser les données de test"""
        self.invoice_service = InvoiceService()
        self.contact_service = ContactService()

        # Créer un contact de test
        self.contact = self.contact_service.create_contact(
            contact_id=None,
            first_name="Client",
            last_name="Test",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789",
            type="client"
        )

    def test_invoice_creation(self):
        """Test la création d'une facture"""
        invoice = self.invoice_service.create_invoice(
            contact_id=self.contact.contact_id,
            name="Facture TEST-001",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789"
        )

        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.name, "Facture TEST-001")
        self.assertEqual(invoice.contact_id.contact_id, self.contact.contact_id)
        self.assertEqual(invoice.status, "En attente")

    def test_invoice_default_status(self):
        """Test que le statut par défaut est 'En attente'"""
        invoice = self.invoice_service.create_invoice(
            contact_id=self.contact.contact_id,
            name="Facture TEST-002",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789"
        )

        self.assertEqual(invoice.status, "En attente")

    def test_invoice_creation_with_invalid_contact(self):
        """Test la création d'une facture avec un contact invalide"""
        with self.assertRaises(ValueError):
            self.invoice_service.create_invoice(
                contact_id=9999,  # Contact qui n'existe pas
                name="Facture TEST-003",
                address="123 Rue Test",
                city="Paris",
                state="Île-de-France",
                zip_code="75001",
                siret="12345678901234",
                email="client@test.com",
                phone="0123456789"
            )

    def test_invoice_creation_with_empty_name(self):
        """Test la création d'une facture avec un nom vide"""
        with self.assertRaises(ValueError):
            self.invoice_service.create_invoice(
                contact_id=self.contact.contact_id,
                name="",
                address="123 Rue Test",
                city="Paris",
                state="Île-de-France",
                zip_code="75001",
                siret="12345678901234",
                email="client@test.com",
                phone="0123456789"
            )

    def test_invoice_creation_with_empty_address(self):
        """Test la création d'une facture avec une adresse vide"""
        with self.assertRaises(ValueError):
            self.invoice_service.create_invoice(
                contact_id=self.contact.contact_id,
                name="Facture TEST-004",
                address="",
                city="Paris",
                state="Île-de-France",
                zip_code="75001",
                siret="12345678901234",
                email="client@test.com",
                phone="0123456789"
            )

    def test_invoice_get_all(self):
        """Test la récupération de toutes les factures"""
        # Créer 3 factures
        for i in range(3):
            self.invoice_service.create_invoice(
                contact_id=self.contact.contact_id,
                name=f"Facture TEST-{i}",
                address="123 Rue Test",
                city="Paris",
                state="Île-de-France",
                zip_code="75001",
                siret="12345678901234",
                email="client@test.com",
                phone="0123456789"
            )

        invoices = self.invoice_service.get_all_invoices()
        self.assertEqual(len(invoices), 3)

    def test_invoice_get_by_id(self):
        """Test la récupération d'une facture par ID"""
        invoice = self.invoice_service.create_invoice(
            contact_id=self.contact.contact_id,
            name="Facture TEST-GetByID",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789"
        )

        retrieved_invoice = self.invoice_service.get_invoice_by_id(invoice.invoice_id)
        self.assertEqual(retrieved_invoice.invoice_id, invoice.invoice_id)
        self.assertEqual(retrieved_invoice.name, "Facture TEST-GetByID")

    def test_invoice_get_by_contact(self):
        """Test la récupération des factures d'un contact"""
        # Créer 2 factures pour le même contact
        for i in range(2):
            self.invoice_service.create_invoice(
                contact_id=self.contact.contact_id,
                name=f"Facture Test Contact-{i}",
                address="123 Rue Test",
                city="Paris",
                state="Île-de-France",
                zip_code="75001",
                siret="12345678901234",
                email="client@test.com",
                phone="0123456789"
            )

        invoices = self.invoice_service.get_invoices_by_contact(self.contact.contact_id)
        self.assertEqual(len(invoices), 2)

    def test_invoice_update(self):
        """Test la mise à jour d'une facture"""
        invoice = self.invoice_service.create_invoice(
            contact_id=self.contact.contact_id,
            name="Facture TEST-Update",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789"
        )

        updated_invoice = self.invoice_service.update_invoice(
            invoice_id=invoice.invoice_id,
            contact_id=self.contact.contact_id,
            name="Facture TEST-Updated",
            address="456 Rue Nouvelle",
            city="Lyon",
            state="Auvergne-Rhône-Alpes",
            zip_code="69000",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789",
            status="réglé"
        )

        self.assertEqual(updated_invoice.name, "Facture TEST-Updated")
        self.assertEqual(updated_invoice.city, "Lyon")
        self.assertEqual(updated_invoice.status, "réglé")

    def test_invoice_delete(self):
        """Test la suppression d'une facture"""
        invoice = self.invoice_service.create_invoice(
            contact_id=self.contact.contact_id,
            name="Facture TEST-Delete",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789"
        )

        invoice_id = invoice.invoice_id
        self.invoice_service.delete_invoice(invoice_id)

        with self.assertRaises(Exception):
            self.invoice_service.get_invoice_by_id(invoice_id)

    def test_invoice_status_choices(self):
        """Test que les statuts disponibles sont correctement définis"""
        invoice = self.invoice_service.create_invoice(
            contact_id=self.contact.contact_id,
            name="Facture TEST-Status",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789"
        )

        # Test statut initial
        self.assertEqual(invoice.status, "En attente")

        # Test mise à jour avec statut payé
        updated = self.invoice_service.update_invoice(
            invoice_id=invoice.invoice_id,
            contact_id=self.contact.contact_id,
            name=invoice.name,
            address=invoice.address,
            city=invoice.city,
            state=invoice.state,
            zip_code=invoice.zip_code,
            siret=invoice.siret,
            email=invoice.email,
            phone=invoice.phone,
            status="réglé"
        )
        self.assertEqual(updated.status, "réglé")


class InvoiceOrderLineTest(TestCase):
    """Tests pour le modèle InvoiceOrderLine et le service InvoiceOrderLineService"""

    def setUp(self):
        """Initialiser les données de test"""
        self.invoice_service = InvoiceService()
        self.contact_service = ContactService()
        self.product_service = ProductService()
        self.invoice_order_line_service = InvoiceOrderLineService()

        # Créer un contact
        self.contact = self.contact_service.create_contact(
            contact_id=None,
            first_name="Client",
            last_name="Test",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789",
            type="client"
        )

        # Créer une facture
        self.invoice = self.invoice_service.create_invoice(
            contact_id=self.contact.contact_id,
            name="Facture TEST",
            address="123 Rue Test",
            city="Paris",
            state="Île-de-France",
            zip_code="75001",
            siret="12345678901234",
            email="client@test.com",
            phone="0123456789"
        )

        # Créer un produit
        self.product = self.product_service.create_product(
            product_id=None,
            product_description="Produit Test",
            price_ht=100.00,
            tax=20,
            price_it=120.00,
            product_type="vente"
        )

    def test_invoice_order_line_creation(self):
        """Test la création d'une ligne de facture"""
        line = self.invoice_order_line_service.create_invoice_order_line(
            invoice_id=self.invoice.invoice_id,
            product_id=self.product.product_id,
            contact_id=self.contact.contact_id,
            price_ht=100.00,
            tax=20,
            price_tax=120.00,
            quantity=2,
            date=date.today()
        )

        self.assertIsNotNone(line)
        self.assertEqual(line.price_ht, 100.00)
        self.assertEqual(line.tax, 20)
        self.assertEqual(line.quantity, 2)

    def test_invoice_order_line_price_calculation(self):
        """Test que le prix TTC est correctement calculé"""
        line = self.invoice_order_line_service.create_invoice_order_line(
            invoice_id=self.invoice.invoice_id,
            product_id=self.product.product_id,
            contact_id=self.contact.contact_id,
            price_ht=100.00,
            tax=20,
            price_tax=120.00,
            quantity=1,
            date=date.today()
        )

        # Vérifier que le prix TTC est correctement calculé (100 + 20% = 120)
        self.assertEqual(line.price_tax, 120.00)

    def test_invoice_order_line_invalid_price_ht(self):
        """Test la création avec un prix HT négatif"""
        with self.assertRaises(ValueError):
            self.invoice_order_line_service.create_invoice_order_line(
                invoice_id=self.invoice.invoice_id,
                product_id=self.product.product_id,
                contact_id=self.contact.contact_id,
                price_ht=-100.00,
                tax=20,
                price_tax=120.00,
                quantity=2,
                date=date.today()
            )

    def test_invoice_order_line_invalid_tax(self):
        """Test la création avec une TVA hors limites"""
        with self.assertRaises(ValueError):
            self.invoice_order_line_service.create_invoice_order_line(
                invoice_id=self.invoice.invoice_id,
                product_id=self.product.product_id,
                contact_id=self.contact.contact_id,
                price_ht=100.00,
                tax=150,  # TVA > 100
                price_tax=250.00,
                quantity=2,
                date=date.today()
            )

    def test_invoice_order_line_invalid_quantity(self):
        """Test la création avec une quantité invalide"""
        with self.assertRaises(ValueError):
            self.invoice_order_line_service.create_invoice_order_line(
                invoice_id=self.invoice.invoice_id,
                product_id=self.product.product_id,
                contact_id=self.contact.contact_id,
                price_ht=100.00,
                tax=20,
                price_tax=120.00,
                quantity=0,  # Quantité <= 0
                date=date.today()
            )

    def test_invoice_order_line_invalid_invoice(self):
        """Test la création avec une facture invalide"""
        with self.assertRaises(ValueError):
            self.invoice_order_line_service.create_invoice_order_line(
                invoice_id=9999,  # Facture qui n'existe pas
                product_id=self.product.product_id,
                contact_id=self.contact.contact_id,
                price_ht=100.00,
                tax=20,
                price_tax=120.00,
                quantity=2,
                date=date.today()
            )

    def test_invoice_order_line_invalid_product(self):
        """Test la création avec un produit invalide"""
        with self.assertRaises(ValueError):
            self.invoice_order_line_service.create_invoice_order_line(
                invoice_id=self.invoice.invoice_id,
                product_id=9999,  # Produit qui n'existe pas
                contact_id=self.contact.contact_id,
                price_ht=100.00,
                tax=20,
                price_tax=120.00,
                quantity=2,
                date=date.today()
            )

    def test_invoice_order_line_invalid_contact(self):
        """Test la création avec un contact invalide"""
        with self.assertRaises(ValueError):
            self.invoice_order_line_service.create_invoice_order_line(
                invoice_id=self.invoice.invoice_id,
                product_id=self.product.product_id,
                contact_id=9999,  # Contact qui n'existe pas
                price_ht=100.00,
                tax=20,
                price_tax=120.00,
                quantity=2,
                date=date.today()
            )

    def test_invoice_order_line_get_all(self):
        """Test la récupération de toutes les lignes"""
        for i in range(3):
            self.invoice_order_line_service.create_invoice_order_line(
                invoice_id=self.invoice.invoice_id,
                product_id=self.product.product_id,
                contact_id=self.contact.contact_id,
                price_ht=100.00 + i * 10,
                tax=20,
                price_tax=120.00 + i * 12,
                quantity=i + 1,
                date=date.today()
            )

        lines = self.invoice_order_line_service.get_all_invoice_order_lines()
        self.assertEqual(len(lines), 3)

    def test_invoice_order_line_get_by_id(self):
        """Test la récupération d'une ligne par ID"""
        line = self.invoice_order_line_service.create_invoice_order_line(
            invoice_id=self.invoice.invoice_id,
            product_id=self.product.product_id,
            contact_id=self.contact.contact_id,
            price_ht=100.00,
            tax=20,
            price_tax=120.00,
            quantity=2,
            date=date.today()
        )

        retrieved_line = self.invoice_order_line_service.get_invoice_order_line_by_id(line.invoice_order_line_id)
        self.assertEqual(retrieved_line.invoice_order_line_id, line.invoice_order_line_id)
        self.assertEqual(retrieved_line.quantity, 2)

    def test_invoice_order_line_get_by_invoice(self):
        """Test la récupération des lignes d'une facture"""
        for i in range(3):
            self.invoice_order_line_service.create_invoice_order_line(
                invoice_id=self.invoice.invoice_id,
                product_id=self.product.product_id,
                contact_id=self.contact.contact_id,
                price_ht=100.00 + i * 10,
                tax=20,
                price_tax=120.00 + i * 12,
                quantity=i + 1,
                date=date.today()
            )

        lines = self.invoice_order_line_service.get_invoice_order_lines_by_invoice(self.invoice.invoice_id)
        self.assertEqual(len(lines), 3)

    def test_invoice_order_line_update(self):
        """Test la mise à jour d'une ligne"""
        line = self.invoice_order_line_service.create_invoice_order_line(
            invoice_id=self.invoice.invoice_id,
            product_id=self.product.product_id,
            contact_id=self.contact.contact_id,
            price_ht=100.00,
            tax=20,
            price_tax=120.00,
            quantity=2,
            date=date.today()
        )

        updated_line = self.invoice_order_line_service.update_invoice_order_line(
            line_id=line.invoice_order_line_id,
            invoice_id=self.invoice.invoice_id,
            product_id=self.product.product_id,
            contact_id=self.contact.contact_id,
            price_ht=150.00,
            tax=20,
            price_tax=180.00,
            quantity=3,
            date=date.today()
        )

        self.assertEqual(updated_line.price_ht, 150.00)
        self.assertEqual(updated_line.quantity, 3)

    def test_invoice_order_line_delete(self):
        """Test la suppression d'une ligne"""
        line = self.invoice_order_line_service.create_invoice_order_line(
            invoice_id=self.invoice.invoice_id,
            product_id=self.product.product_id,
            contact_id=self.contact.contact_id,
            price_ht=100.00,
            tax=20,
            price_tax=120.00,
            quantity=2,
            date=date.today()
        )

        line_id = line.invoice_order_line_id
        self.invoice_order_line_service.delete_invoice_order_line(line_id)

        with self.assertRaises(Exception):
            self.invoice_order_line_service.get_invoice_order_line_by_id(line_id)

    def test_invoice_order_line_multiple_products(self):
        """Test la création de plusieurs lignes avec des produits différents"""
        # Créer un second produit
        product2 = self.product_service.create_product(
            product_id=None,
            product_description="Produit Test 2",
            price_ht=200.00,
            tax=20,
            price_it=240.00,
            product_type="vente"
        )

        line1 = self.invoice_order_line_service.create_invoice_order_line(
            invoice_id=self.invoice.invoice_id,
            product_id=self.product.product_id,
            contact_id=self.contact.contact_id,
            price_ht=100.00,
            tax=20,
            price_tax=120.00,
            quantity=1,
            date=date.today()
        )

        line2 = self.invoice_order_line_service.create_invoice_order_line(
            invoice_id=self.invoice.invoice_id,
            product_id=product2.product_id,
            contact_id=self.contact.contact_id,
            price_ht=200.00,
            tax=20,
            price_tax=240.00,
            quantity=1,
            date=date.today()
        )

        lines = self.invoice_order_line_service.get_invoice_order_lines_by_invoice(self.invoice.invoice_id)
        self.assertEqual(len(lines), 2)

        # Vérifier que les lignes sont différentes
        self.assertEqual(line1.product_id.product_id, self.product.product_id)
        self.assertEqual(line2.product_id.product_id, product2.product_id)

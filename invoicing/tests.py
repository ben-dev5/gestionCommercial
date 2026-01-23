from django.test import TestCase

from invoicing.models import InvoiceOrderLine


# Create your tests here.
class InvoiceOrderLineTest(TestCase):
    def test_price(self):
        self.assertEqual(InvoiceOrderLine.objects.all().count(), 0)
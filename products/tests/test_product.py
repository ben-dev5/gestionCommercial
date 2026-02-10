from django.test import TestCase
from django.db import IntegrityError

from products.services.product_service import ProductService


class ProductValidateFields(TestCase):
    def setUp(self):
        self.service = ProductService()
        self.product = self.service.create_product(
            product_id = 1,
            product_description = "séminaire de formation",
            price_ht = 1000,
            tax = 20,
            price_it = 1200
        )

    def test_validate_product_field(self):
        # test que les champs sont pas vide
        self.assertIsNotNone(self.product.product_description)
        self.assertIsNotNone(self.product.price_ht)
        self.assertIsNotNone(self.product.tax)
        self.assertIsNotNone(self.product.price_it)
        self.assertIsNotNone(self.product.product_id)

        # test que les champs sont bien correpondants
        self.assertEqual(self.product.product_description, "séminaire de formation")
        self.assertEqual(self.product.price_ht, 1000)
        self.assertEqual(self.product.tax, 20)
        self.assertEqual(self.product.price_it, 1200)
        self.assertEqual(self.product.product_id, 1)

    def test_price_it_sum(self):
        # test prix it est bien égale à la somme
        expected_price_it = self.product.price_ht * (1 + self.product.tax / 100)
        self.assertEqual(self.product.price_it, expected_price_it)

    def test_description_is_unique(self):
        # test que la description du produit est unique
        with self.assertRaises(IntegrityError):
            self.service.create_product(
                product_id = 2,
                product_description = "séminaire de formation",
                price_ht = 2000,
                tax = 20,
                price_it = 2400
            )

    def test_price_ht_must_be_positive(self):
        # test que le prix HT doit être positif
        with self.assertRaises(ValueError):
            self.service.create_product(
                product_id=3,
                product_description="produit négatif",
                price_ht=-100,
                tax=20,
                price_it=0
            )

    def test_tax_must_be_between_0_and_100(self):
        # test que la taxe doit être entre 0 et 100%
        with self.assertRaises(ValueError):
            self.service.create_product(
                product_id=4,
                product_description="taxe invalide",
                price_ht=1000,
                tax=150,
                price_it=2500
            )

    def test_product_id_must_be_positive(self):
        # test que l'ID du produit doit être positif
        with self.assertRaises(ValueError):
            self.service.create_product(
                product_id=-1,
                product_description="id négatif",
                price_ht=1000,
                tax=20,
                price_it=1200
            )



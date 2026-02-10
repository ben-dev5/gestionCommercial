from django.test import TestCase
from django.db import IntegrityError
from decimal import Decimal

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


class ProductUpdateTests(TestCase):
    def setUp(self):
        self.service = ProductService()
        self.product = self.service.create_product(
            product_id=1,
            product_description="produit original",
            price_ht=1000,
            tax=20,
            price_it=1200
        )

    def test_update_product_price(self):
        # test modification du prix HT
        updated_product = self.service.update_product(
            product_id=self.product.product_id,
            product_description="produit original",
            price_ht=1500,
            tax=20,
            price_it=1800
        )
        self.assertEqual(updated_product.price_ht, 1500)

    def test_update_product_tax(self):
        # test modification de la taxe
        updated_product = self.service.update_product(
            product_id=self.product.product_id,
            product_description="produit original",
            price_ht=1000,
            tax=10,
            price_it=1100
        )
        self.assertEqual(updated_product.tax, 10)

    def test_update_product_description(self):
        # test modification de la description
        updated_product = self.service.update_product(
            product_id=self.product.product_id,
            product_description="nouvelle description",
            price_ht=1000,
            tax=20,
            price_it=1200
        )
        self.assertEqual(updated_product.product_description, "nouvelle description")


class ProductDeleteTests(TestCase):
    def setUp(self):
        self.service = ProductService()
        self.product = self.service.create_product(
            product_id=1,
            product_description="produit à supprimer",
            price_ht=1000,
            tax=20,
            price_it=1200
        )

    def test_delete_product(self):
        # test suppression d'un produit
        product_id = self.product.product_id
        self.service.delete_product(product_id)
        with self.assertRaises(Exception):
            self.service.get_product_by_id(product_id)


class ProductRetrievalTests(TestCase):
    def setUp(self):
        self.service = ProductService()
        self.product1 = self.service.create_product(
            product_id=1,
            product_description="produit 1",
            price_ht=1000,
            tax=20,
            price_it=1200
        )
        self.product2 = self.service.create_product(
            product_id=2,
            product_description="produit 2",
            price_ht=500,
            tax=5.5,
            price_it=527.5
        )

    def test_get_product_by_id(self):
        # test récupération d'un produit par ID
        product = self.service.get_product_by_id(self.product1.product_id)
        self.assertEqual(product.product_description, "produit 1")

    def test_get_all_products(self):
        # test récupération de tous les produits
        products = self.service.get_all_products()
        self.assertEqual(len(products), 2)

    def test_get_product_by_id_returns_correct_product(self):
        # test que la récupération retourne le bon produit
        product = self.service.get_product_by_id(self.product2.product_id)
        self.assertEqual(product.product_id, 2)
        self.assertEqual(product.price_ht, 500)


class ProductBoundaryTests(TestCase):
    def setUp(self):
        self.service = ProductService()

    def test_zero_price_ht(self):
        # test que le prix HT peut être zéro
        product = self.service.create_product(
            product_id=1,
            product_description="produit gratuit",
            price_ht=0,
            tax=20,
            price_it=0
        )
        self.assertEqual(product.price_ht, 0)

    def test_zero_tax(self):
        # test que la taxe peut être zéro
        product = self.service.create_product(
            product_id=2,
            product_description="sans taxe",
            price_ht=1000,
            tax=0,
            price_it=1000
        )
        self.assertEqual(product.tax, 0)

    def test_high_price(self):
        # test avec un prix très élevé
        product = self.service.create_product(
            product_id=3,
            product_description="produit cher",
            price_ht=999999.99,
            tax=20,
            price_it=1199999.99
        )
        self.assertGreater(product.price_ht, 100000)

    def test_decimal_tax(self):
        # test avec une taxe décimale
        product = self.service.create_product(
            product_id=4,
            product_description="taxe décimale",
            price_ht=1000,
            tax=5.5,
            price_it=1055
        )
        self.assertEqual(product.tax, Decimal('5.5'))


class ProductCalculationTests(TestCase):
    def setUp(self):
        self.service = ProductService()

    def test_price_calculation_0_percent_tax(self):
        # test calcul avec 0% de taxe
        product = self.service.create_product(
            product_id=1,
            product_description="taxe 0%",
            price_ht=100,
            tax=0,
            price_it=100
        )
        self.assertEqual(product.price_it, 100)

    def test_price_calculation_5_5_percent_tax(self):
        # test calcul avec 5.5% de taxe
        product = self.service.create_product(
            product_id=2,
            product_description="taxe 5.5%",
            price_ht=100,
            tax=5.5,
            price_it=105.5
        )
        self.assertEqual(product.price_it, 105.5)

    def test_price_calculation_10_percent_tax(self):
        # test calcul avec 10% de taxe
        product = self.service.create_product(
            product_id=3,
            product_description="taxe 10%",
            price_ht=100,
            tax=10,
            price_it=110
        )
        self.assertEqual(product.price_it, 110)

    def test_price_calculation_20_percent_tax(self):
        # test calcul avec 20% de taxe
        product = self.service.create_product(
            product_id=4,
            product_description="taxe 20%",
            price_ht=100,
            tax=20,
            price_it=120
        )
        self.assertEqual(product.price_it, 120)

    def test_price_calculation_high_values(self):
        # test calcul avec valeurs élevées
        product = self.service.create_product(
            product_id=5,
            product_description="valeurs élevées",
            price_ht=1000,
            tax=20,
            price_it=1200
        )
        self.assertEqual(product.price_it, 1200)

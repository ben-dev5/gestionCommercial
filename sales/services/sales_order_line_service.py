from sales.repositories.sales_order_line_repository import SalesOrderLineRepository
from sales.services.sales_order_service import SalesOrderService
from products.services.product_service import ProductService
from commons.services.contact_service import ContactService


class SalesOrderLineService:
    def __init__(self):
        self.repo = SalesOrderLineRepository()
        self.sales_order_service = SalesOrderService()
        self.product_service = ProductService()
        self.contact_service = ContactService()

    def validate_sales_order_line_data(self, sales_order_id, product_id, contact_id, price_ht, tax, quantity, date, genre):
        try:
            self.sales_order_service.get_sales_order_by_id(sales_order_id)
        except:
            raise ValueError("La commande n'existe pas")

        # Vérifier que le produit existe
        try:
            product = self.product_service.get_product_by_id(product_id)
        except:
            raise ValueError("Le produit n'existe pas")

        # Vérifier que le produit est de type vente ou achat/vente
        if product.product_type not in ['vente', 'achat/vente']:
            raise ValueError("Ce produit n'est pas destiné à la vente")

        # Vérifier que price_ht est positif
        if price_ht < 0:
            raise ValueError("price_ht doit être positif")

        # Vérifier que tax est entre 0 et 100
        if tax < 0 or tax > 100:
            raise ValueError("tax doit être entre 0 et 100")

        # Vérifier que quantity est positif
        if quantity <= 0:
            raise ValueError("La quantité doit être positive")

        # Vérifier que le genre n'est pas vide
        if not genre or genre.strip() == "":
            raise ValueError("Le genre ne peut pas être vide")

    def create_sales_order_line(self, sales_order_id, product_id, contact_id, price_ht, tax, price_it, quantity, date, genre):
        self.validate_sales_order_line_data(sales_order_id, product_id, contact_id, price_ht, tax, quantity, date, genre)
        # Récupérer les objets
        sales_order = self.sales_order_service.get_sales_order_by_id(sales_order_id)
        product = self.product_service.get_product_by_id(product_id)
        contact = self.contact_service.get_contact_by_id(contact_id)

        return self.repo.create_sales_order_line(sales_order, product, contact, price_ht, tax, price_it, quantity, date, genre)

    def delete_sales_order_line(self, sales_order_line_id):
        return self.repo.delete_sales_order_line(sales_order_line_id)

    def get_all_sales_order_lines(self):
        return self.repo.get_all_sales_order_lines()

    def get_sales_order_line_by_id(self, sales_order_line_id):
        return self.repo.get_sales_order_line_by_id(sales_order_line_id)

    def get_sales_order_lines_by_order(self, sales_order_id):
        return self.repo.get_sales_order_lines_by_order(sales_order_id)

    def update_sales_order_line(self, sales_order_line_id, sales_order_id, product_id, contact_id, price_ht, tax, quantity, date, genre):
        self.validate_sales_order_line_data(sales_order_id, product_id, contact_id, price_ht, tax, quantity, date, genre)
        sales_order = self.sales_order_service.get_sales_order_by_id(sales_order_id)
        product = self.product_service.get_product_by_id(product_id)
        contact = self.contact_service.get_contact_by_id(contact_id)

        return self.repo.update_sales_order_line(sales_order_line_id, sales_order, product, contact, price_ht, tax, quantity, date, genre)


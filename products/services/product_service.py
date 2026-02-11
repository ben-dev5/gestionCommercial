from products.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def validate_product_data(self, product_id, product_description, price_ht, tax, price_it, product_type):
        # Vérifier que product_id est positif (si fourni)
        if product_id is not None and product_id < 0:
            raise ValueError("product_id doit être positif")

        # Vérifier que la description n'est pas vide
        if not product_description or product_description.strip() == "":
            raise ValueError("product_description ne peut pas être vide")

        # Vérifier que price_ht est positif
        if price_ht < 0:
            raise ValueError("price_ht doit être positif")

        # Vérifier que tax est entre 0 et 100
        if tax < 0 or tax > 100:
            raise ValueError("tax doit être entre 0 et 100")

        # Vérifier que price_it correspond au calcul (tolérance de 0.01 pour arrondi)
        expected_price_it = price_ht * (1 + tax / 100)
        if abs(price_it - expected_price_it) > 0.01:
            raise ValueError(f"price_it doit être égal à {round(expected_price_it, 2)}")

        # Vérifier que product_type est valide
        valid_types = ['achat', 'vente', 'achat/vente']
        if product_type not in valid_types:
            raise ValueError(f"product_type doit être l'un de: {', '.join(valid_types)}")

    def create_product(self, product_id, product_description, price_ht, tax, price_it, product_type):
        self.validate_product_data(product_id, product_description, price_ht, tax, price_it, product_type)
        return self.repo.create_product(product_id, product_description, price_ht, tax, price_it, product_type)

    def delete_product(self, product_id):
        return self.repo.delete_product(product_id)

    def get_all_products(self):
        return self.repo.get_all_products()

    def get_product_by_id(self, product_id):
        return self.repo.get_product_by_id(product_id)

    def update_product(self, product_id, product_description, price_ht, tax, price_it, product_type):
        self.validate_product_data(product_id, product_description, price_ht, tax, price_it, product_type)
        return self.repo.update_product(product_id, product_description, price_ht, tax, price_it, product_type)

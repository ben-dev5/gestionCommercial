from sales.repositories.sales_order_repository import SalesOrderRepository
from commons.services.contact_service import ContactService


class SalesOrderService:
    def __init__(self):
        self.repo = SalesOrderRepository()
        self.contact_service = ContactService()

    def validate_sales_order_data(self, contact_id, genre, order_type):
        # Vérifier que le contact existe
        try:
            contact = self.contact_service.get_contact_by_id(contact_id)
        except:
            raise ValueError("Le contact n'existe pas")

        # contact type client vérifié
        if contact.type != 'client':
            raise ValueError("Le contact doit être de type 'Client' pour créer un devis/commande")

        # Vérifier que le genre n'est pas vide
        if not genre or genre.strip() == "":
            raise ValueError("Le genre ne peut pas être vide")

        # Vérifier que le type est valide
        valid_types = ['Devis', 'Commande']
        if order_type not in valid_types:
            raise ValueError(f"Le type doit être l'un de: {', '.join(valid_types)}")


    def create_sales_order(self, contact_id, genre, order_type):
        self.validate_sales_order_data(contact_id, genre, order_type)
        contact = self.contact_service.get_contact_by_id(contact_id)
        return self.repo.create_sales_order(contact, genre, order_type)

    def delete_sales_order(self, sales_order_id):
        return self.repo.delete_sales_order(sales_order_id)

    def get_all_sales_orders(self):
        return self.repo.get_all_sales_orders()

    def get_sales_order_by_id(self, sales_order_id):
        return self.repo.get_sales_order_by_id(sales_order_id)

    def get_sales_orders_by_type(self, order_type):
        return self.repo.get_sales_orders_by_type(order_type)

    def get_sales_orders_by_contact(self, contact_id):
        return self.repo.get_sales_orders_by_contact(contact_id)

    def update_sales_order(self, sales_order_id, contact_id, genre, order_type):
        self.validate_sales_order_data(contact_id, genre, order_type)
        contact = self.contact_service.get_contact_by_id(contact_id)
        return self.repo.update_sales_order(sales_order_id, contact, genre, order_type)


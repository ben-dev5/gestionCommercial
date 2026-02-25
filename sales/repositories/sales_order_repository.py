from sales.models.sales_order_models import SalesOrder


class SalesOrderRepository:

    def create_sales_order(self, contact, genre, order_type):
        return SalesOrder.objects.create(
            contact_id=contact,
            genre=genre,
            type=order_type
        )

    def delete_sales_order(self, sales_order_id):
        sales_order = SalesOrder.objects.get(sales_order_id=sales_order_id)
        sales_order.delete()
        return True

    def get_all_sales_orders(self):
        return SalesOrder.objects.all().order_by('sales_order_id')

    def get_sales_order_by_id(self, sales_order_id):
        return SalesOrder.objects.get(sales_order_id=sales_order_id)

    def get_sales_orders_by_type(self, order_type):
        return SalesOrder.objects.filter(type=order_type).order_by('sales_order_id')

    def get_sales_orders_by_contact(self, contact_id):
        return SalesOrder.objects.filter(contact_id=contact_id).order_by('sales_order_id')

    def update_sales_order(self, sales_order_id, contact, genre, order_type):
        sales_order = SalesOrder.objects.get(sales_order_id=sales_order_id)
        sales_order.contact_id = contact
        sales_order.genre = genre
        sales_order.type = order_type
        sales_order.save()
        return sales_order

    def save(self, sales_order):
        sales_order.save()
        return sales_order

    def get_by_public_hash(self, public_hash):
        return SalesOrder.objects.get(public_hash=public_hash)


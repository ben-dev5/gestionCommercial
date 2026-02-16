from sales.models.sales_order_line_models import SalesOrderLine


class SalesOrderLineRepository:

    def create_sales_order_line(self, sales_order, product, contact, price_ht, tax, price_it, quantity, date, genre):
        return SalesOrderLine.objects.create(
            sales_order_id=sales_order,
            product_id=product,
            contact_id=contact,
            price_ht=price_ht,
            tax=tax,
            price_it=price_it,
            quantity=quantity,
            date=date,
            genre=genre
        )

    def delete_sales_order_line(self, sales_order_line_id):
        sales_order_line = SalesOrderLine.objects.get(sales_order_line_id=sales_order_line_id)
        sales_order_line.delete()
        return True

    def get_all_sales_order_lines(self):
        return SalesOrderLine.objects.all().order_by('sales_order_line_id')

    def get_sales_order_line_by_id(self, sales_order_line_id):
        return SalesOrderLine.objects.get(sales_order_line_id=sales_order_line_id)

    def get_sales_order_lines_by_order(self, sales_order_id):
        return SalesOrderLine.objects.filter(sales_order_id=sales_order_id).order_by('sales_order_line_id')

    def update_sales_order_line(self, sales_order_line_id, sales_order, product, contact, price_ht, tax, price_it, quantity, date, genre):
        sales_order_line = SalesOrderLine.objects.get(sales_order_line_id=sales_order_line_id)
        sales_order_line.sales_order_id = sales_order
        sales_order_line.product_id = product
        sales_order_line.contact_id = contact
        sales_order_line.price_ht = price_ht
        sales_order_line.tax = tax
        sales_order_line.price_it = price_it
        sales_order_line.quantity = quantity
        sales_order_line.date = date
        sales_order_line.genre = genre
        sales_order_line.save()
        return sales_order_line


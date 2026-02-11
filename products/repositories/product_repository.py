from products.models import Product

class ProductRepository:

    def create_product(self, product_id, product_description, price_ht, tax, price_it, product_type):
        return Product.objects.create(
            product_id=product_id,
            product_description=product_description,
            price_ht=price_ht,
            tax=tax,
            price_it=price_it,
            product_type=product_type
        )

    def delete_product(self, product_id):
        product = Product.objects.get(product_id=product_id)
        product.delete()
        return True

    def get_all_products(self):
        return Product.objects.all().order_by('product_description')

    def get_product_by_id(self, product_id):
        return Product.objects.get(product_id=product_id)

    def update_product(self, product_id, product_description, price_ht, tax, price_it, product_type):
        product = Product.objects.get(product_id=product_id)
        product.product_description = product_description
        product.price_ht = price_ht
        product.tax = tax
        product.price_it = price_it
        product.product_type = product_type
        product.save()
        return product
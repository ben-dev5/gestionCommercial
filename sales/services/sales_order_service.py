from sales.repositories.sales_order_repository import SalesOrderRepository
from commons.services.contact_service import ContactService
from django.urls import reverse
from django.utils import timezone
import hashlib
from datetime import timedelta


class SalesOrderService:
    def __init__(self):
        self.repo = SalesOrderRepository()
        self.contact_service = ContactService()
        self.HASH_EXPIRATION_DAYS = 7

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

    # Méthodes pour la signature du devis par le client
    def generate_public_hash(self, sales_order):
        """Génère un hash public unique pour partager le devis"""
        # Vérifier que le devis peut être partagé
        if sales_order.status == 'Signé' or sales_order.type == 'Commande':
            raise ValueError("Ce devis est déjà signé et ne peut pas être partagé")

        # Générer un hash unique
        unique_string = f"{sales_order.sales_order_id}-{timezone.now().isoformat()}"
        public_hash = hashlib.sha256(unique_string.encode()).hexdigest()

        # Définir la date d'expiration (7 jours par défaut)
        expiration_date = timezone.now() + timedelta(days=self.HASH_EXPIRATION_DAYS)

        # Mettre à jour le devis
        sales_order.public_hash = public_hash
        sales_order.public_hash_expires_at = expiration_date
        self.repo.save(sales_order)

        return public_hash

    def is_hash_valid(self, sales_order):
        """Vérifie si le hash est encore valide"""
        if not sales_order.public_hash:
            return False

        # Vérifier l'expiration
        if sales_order.public_hash_expires_at:
            if timezone.now() > sales_order.public_hash_expires_at:
                self.invalidate_hash(sales_order)
                return False

        return True

    def invalidate_hash(self, sales_order):
        """Invalide le hash public"""
        sales_order.public_hash = None
        sales_order.public_hash_expires_at = None
        self.repo.save(sales_order)

    def get_sales_order_by_hash(self, public_hash):
        """Récupère un devis par son hash public"""
        if not public_hash:
            raise ValueError("Hash public vide ou invalide")

        try:
            sales_order = self.repo.get_by_public_hash(public_hash)
        except Exception as e:
            raise ValueError(f"Devis non trouvé avec ce lien : {str(e)}")

        # Vérifier que le hash est valide
        if not self.is_hash_valid(sales_order):
            raise ValueError("Ce lien a expiré ou n'est pas valide")

        return sales_order

    def sign_sales_order(self, sales_order, client_ip=None):
        """Marque le devis comme signé par le client"""
        if sales_order.status == 'Signé':
            raise ValueError("Ce devis/commande est déjà signé")

        # Mettre à jour le statut
        sales_order.status = 'Signé'
        sales_order.signed_at = timezone.now()
        sales_order.signed_ip = client_ip
        sales_order.public_hash = None
        sales_order.public_hash_expires_at = None

        self.repo.save(sales_order)
        return sales_order

    def build_public_url(self, request, sales_order_id, public_hash):
        """Construit l'URL publique pour partager le devis"""
        base_url = request.build_absolute_uri(reverse('sales:sales_order_detail', args=[sales_order_id]))
        return f"{base_url}?hash={public_hash}"

    def has_public_hash(self, sales_order):
        """Vérifie si le devis a un hash public"""
        return getattr(sales_order, 'public_hash', None) is not None

    def get_public_hash(self, sales_order):
        """Récupère le hash public du devis"""
        return getattr(sales_order, 'public_hash', None)





from datetime import datetime
from decimal import Decimal


from sales.services.sales_order_service import SalesOrderService
from sales.services.sales_order_line_service import SalesOrderLineService
from invoicing.services.invoice_service import InvoiceService
from invoicing.services.invoice_order_line_service import InvoiceOrderLineService
from payment.services.payment_service import PaymentService
from commons.services.contact_service import ContactService


class DashboardService:


    def __init__(self):
        self.sales_order_service = SalesOrderService()
        self.sales_order_line_service = SalesOrderLineService()
        self.invoice_service = InvoiceService()
        self.invoice_order_line_service = InvoiceOrderLineService()
        self.payment_service = PaymentService()
        self.contact_service = ContactService()

    def get_monthly_revenue(self):

        # En prenant en compte les status de paiements avec filtre sur le mois courant
        payments = self.payment_service.get_all_payments()

        today = datetime.now()
        current_month = today.month
        current_year = today.year

        total_revenue = Decimal('0.00')
        for payment in payments:
            # Vérifier que le paiement est "Payé" et du mois courant
            if payment.state_payment == 'Payé' and hasattr(payment, 'created_at') and payment.created_at:
                payment_date = payment.created_at if isinstance(payment.created_at, datetime) else datetime.fromisoformat(str(payment.created_at))
                if payment_date.month == current_month and payment_date.year == current_year:
                    total_revenue += Decimal(str(payment.amount))

        return float(total_revenue)

    def get_sales_evolution(self):
        payments = self.payment_service.get_all_payments()

        evolution_data = {}
        today = datetime.now()

        # Créer les labels pour les 6 derniers mois (en remontant dans le temps)
        for i in range(6):
            # Calculer la date du premier jour du mois
            if i == 0:
                # Mois courant
                month_date = today.replace(day=1)
            else:
                # Mois précédents
                month_date = today.replace(day=1)
                for _ in range(i):
                    # Reculer d'un mois
                    if month_date.month == 1:
                        month_date = month_date.replace(year=month_date.year - 1, month=12)
                    else:
                        month_date = month_date.replace(month=month_date.month - 1)

            month_label = month_date.strftime('%b %Y')
            evolution_data[month_label] = {
                'month': month_date.month,
                'year': month_date.year,
                'revenue': Decimal('0.00')
            }

        # Remplir avec les paiements réglés
        for payment in payments:
            if payment.state_payment == 'Payé' and hasattr(payment, 'created_at') and payment.created_at:
                payment_date = payment.created_at if isinstance(payment.created_at, datetime) else datetime.fromisoformat(str(payment.created_at))
                month_label = payment_date.strftime('%b %Y')

                if month_label in evolution_data:
                    evolution_data[month_label]['revenue'] += Decimal(str(payment.amount))

        # Retourner au format dictionnaire simple {mois: revenue}
        return {k: float(v['revenue']) for k, v in evolution_data.items()}

    def get_top_5_clients(self):
        payments = self.payment_service.get_all_payments()

        client_revenue = {}

        for payment in payments:
            # Vérifier que le paiement est "Payé"
            if payment.state_payment == 'Payé':
                try:
                    invoice = payment.invoice_id
                    contact_id = invoice.contact_id.contact_id
                    contact = self.contact_service.get_contact_by_id(contact_id)

                    if contact_id not in client_revenue:
                        client_revenue[contact_id] = {
                            'contact': contact,
                            'revenue': Decimal('0.00')
                        }

                    client_revenue[contact_id]['revenue'] += Decimal(str(payment.amount))
                except:
                    pass

        sorted_clients = sorted(
            client_revenue.values(),
            key=lambda x: x['revenue'],
            reverse=True
        )[:5]

        return [
            {
                'name': f"{client['contact'].first_name} {client['contact'].last_name}",
                'revenue': float(client['revenue']),
                'contact_id': client['contact'].contact_id
            }
            for client in sorted_clients
        ]

    def get_unconverted_quotes(self):
        sales_orders = self.sales_order_service.get_all_sales_orders()
        invoices = self.invoice_service.get_all_invoices()

        converted_quote_ids = set()
        for invoice in invoices:
            if hasattr(invoice, 'sales_order_id') and invoice.sales_order_id:
                converted_quote_ids.add(invoice.sales_order_id.sales_order_id)

        unconverted_quotes = []
        for sales_order in sales_orders:
            if sales_order.type == 'Devis':
                if sales_order.sales_order_id not in converted_quote_ids:
                    try:
                        lines = self.sales_order_line_service.get_sales_order_lines_by_order(sales_order.sales_order_id)
                        if len(lines) > 0:
                            unconverted_quotes.append({
                                'id': sales_order.sales_order_id,
                                'contact': f"{sales_order.contact_id.first_name} {sales_order.contact_id.last_name}",
                                'genre': sales_order.genre,
                                'created_at': sales_order.created_at if hasattr(sales_order, 'created_at') else 'N/A',
                                'lines_count': len(lines)
                            })
                    except:
                        pass

        return unconverted_quotes

    def get_dashboard_stats(self):
        return {
            'monthly_revenue': self.get_monthly_revenue(),
            'sales_evolution': self.get_sales_evolution(),
            'top_5_clients': self.get_top_5_clients(),
            'unconverted_quotes': self.get_unconverted_quotes(),
        }
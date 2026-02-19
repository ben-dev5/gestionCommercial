from datetime import datetime, timedelta
from decimal import Decimal

from django.core.cache import cache

from sales.services.sales_order_service import SalesOrderService
from sales.services.sales_order_line_service import SalesOrderLineService
from invoicing.services.invoice_service import InvoiceService
from invoicing.services.invoice_order_line_service import InvoiceOrderLineService
from commons.services.contact_service import ContactService


class DashboardService:
    """Service pour dashboard"""

    def __init__(self):
        self.sales_order_service = SalesOrderService()
        self.sales_order_line_service = SalesOrderLineService()
        self.invoice_service = InvoiceService()
        self.invoice_order_line_service = InvoiceOrderLineService()
        self.contact_service = ContactService()

    def get_monthly_revenue(self):
        """Retourne le chiffre d'affaires du mois courant (factures existantes uniquement et réglées)"""
        invoices = self.invoice_service.get_all_invoices()

        today = datetime.now()
        current_month = today.month
        current_year = today.year

        total_revenue = Decimal('0.00')
        for invoice in invoices:
            # Vérifier que la facture est réglée et du mois courant
            if invoice.status == 'réglé' and hasattr(invoice, 'created_at') and invoice.created_at:
                invoice_date = invoice.created_at if isinstance(invoice.created_at, datetime) else datetime.fromisoformat(str(invoice.created_at))
                if invoice_date.month == current_month and invoice_date.year == current_year:
                    try:
                        lines = self.invoice_order_line_service.get_invoice_order_lines_by_invoice(invoice.invoice_id)
                        for line in lines:
                            total_revenue += Decimal(str(line.price_tax))
                    except:
                        pass

        return float(total_revenue)

    def get_sales_evolution(self):
        """Retourne l'évolution des ventes sur 6 mois (factures existantes uniquement et réglées)"""
        invoices = self.invoice_service.get_all_invoices()

        evolution_data = {}
        today = datetime.now()

        # Créer les labels pour 6 mois précédents
        for i in range(6):
            month_date = today - timedelta(days=today.day - 1)
            for _ in range(i):
                if month_date.month == 1:
                    month_date = month_date.replace(year=month_date.year - 1, month=12)
                else:
                    month_date = month_date.replace(month=month_date.month - 1)

            month_label = month_date.strftime('%B %Y')
            evolution_data[month_label] = {'month': month_date.month, 'year': month_date.year, 'revenue': Decimal('0.00')}

        # Remplir avec les factures existantes et réglées
        for invoice in invoices:
            if invoice.status == 'réglé' and hasattr(invoice, 'created_at') and invoice.created_at:
                invoice_date = invoice.created_at if isinstance(invoice.created_at, datetime) else datetime.fromisoformat(str(invoice.created_at))
                month_label = invoice_date.strftime('%B %Y')

                if month_label in evolution_data:
                    try:
                        lines = self.invoice_order_line_service.get_invoice_order_lines_by_invoice(invoice.invoice_id)
                        for line in lines:
                            evolution_data[month_label]['revenue'] += Decimal(str(line.price_tax))
                    except:
                        pass

        return {k: float(v['revenue']) for k, v in evolution_data.items()}

    def get_top_5_clients(self):
        """Retourne les 5 clients avec le plus gros CA (factures existantes uniquement et réglées)"""
        invoices = self.invoice_service.get_all_invoices()

        client_revenue = {}

        for invoice in invoices:
            # Vérifier que la facture est réglée
            if invoice.status == 'réglé':
                try:
                    contact_id = invoice.contact_id.contact_id
                    contact = self.contact_service.get_contact_by_id(contact_id)

                    if contact_id not in client_revenue:
                        client_revenue[contact_id] = {
                            'contact': contact,
                            'revenue': Decimal('0.00')
                        }

                    lines = self.invoice_order_line_service.get_invoice_order_lines_by_invoice(invoice.invoice_id)
                    for line in lines:
                        client_revenue[contact_id]['revenue'] += Decimal(str(line.price_tax))
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
        """Retourne les devis non transformés en commandes/factures"""
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
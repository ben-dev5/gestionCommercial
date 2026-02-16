from django.views.generic import TemplateView

from dashboard.services.dashboard_service import DashboardService


class DashboardView(TemplateView):
    """Vue principale du dashboard"""
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = DashboardService()

        try:
            stats = service.get_dashboard_stats()

            context['monthly_revenue'] = stats['monthly_revenue']
            context['sales_evolution'] = stats['sales_evolution']
            context['top_5_clients'] = stats['top_5_clients']
            context['unconverted_quotes'] = stats['unconverted_quotes']

        except Exception as e:
            context['error'] = f"Erreur lors du chargement des statistiques : {str(e)}"

        return context

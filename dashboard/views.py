from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import json
from dashboard.services.dashboard_service import DashboardService


class DashboardView(TemplateView):
    """Vue principale du dashboard"""
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = DashboardService()

        try:
            # Récupérer les stats avec le statut par défaut "Payé"
            stats = service.get_dashboard_stats('Payé')

            context['monthly_revenue'] = stats['monthly_revenue']
            context['sales_evolution'] = json.dumps(stats['sales_evolution'])
            context['top_5_clients'] = stats['top_5_clients']
            context['unconverted_quotes'] = stats['unconverted_quotes']

        except Exception as e:
            context['error'] = f"Erreur lors du chargement des statistiques : {str(e)}"

        return context

    def post(self, request, *args, **kwargs):
        # Gérer la requête AJAX pour le filtrage par statut de paiement
        service = DashboardService()
        payment_status = request.POST.get('payment_status') or request.GET.get('payment_status')

        try:
            if payment_status:
                # Récupérer les stats filtrées par le statut demandé
                stats = service.get_dashboard_stats(payment_status)

                return JsonResponse({
                    'monthly_revenue': stats['monthly_revenue'],
                    'sales_evolution': stats['sales_evolution'],
                    'top_5_clients': stats['top_5_clients'],
                })
            else:
                return JsonResponse({'error': 'Statut de paiement non spécifié'}, status=400)

        except Exception as e:
            return JsonResponse({'error': f"Erreur lors du filtrage des données : {str(e)}"}, status=500)
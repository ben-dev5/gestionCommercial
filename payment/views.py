from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from payment.services.payment_service import PaymentService


class PaymentView(TemplateView):
    template_name = 'payment/payment.html'

    def get_context_data(self, invoice_id=None, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_service = PaymentService()

        # Récupérer invoice_id depuis les paramètres de requête ou passé en paramètre
        if not invoice_id:
            invoice_id = self.request.GET.get('invoice_id')

        try:
            # Affiche seulement les paiements de cette facture spécifique
            if invoice_id:
                context['payments'] = payment_service.get_payments_by_invoice_id(invoice_id)
                # Récupérer le statut de la facture
                context['invoice'] = type('obj', (object,), {'status': payment_service.get_invoice_status(invoice_id)})()
            else:
                context['payments'] = None
                context['invoice'] = None
            context['invoice_id'] = invoice_id
        except:
            context['payments'] = None
            context['invoice'] = None
            context['invoice_id'] = invoice_id

        return context

    def post(self, request, *args, **kwargs):
        payment_method = request.POST.get('payment_method')
        state_payment = request.POST.get('state_payment')
        invoice_id = request.POST.get('invoice_id')
        # récupération du status de la facture associée au paiement pour vérifier si le paiement est autorisé ou pas
        amount = request.POST.get('amount')

        payment_service = PaymentService()
        try:
            # Vérifier que tous les champs sont remplis
            if not all([payment_method, state_payment, invoice_id, amount]):
                context = self.get_context_data(invoice_id=invoice_id)
                context['error'] = 'Tous les champs sont obligatoires'
                return render(request, self.template_name, context)

            # Convertir amount en nombre
            try:
                amount = float(amount)
            except ValueError:
                context = self.get_context_data(invoice_id=invoice_id)
                context['error'] = 'Le montant doit être un nombre valide'
                return render(request, self.template_name, context)

            # Créer le paiement
            result = payment_service.create_payment(payment_method, state_payment, invoice_id, amount)

            # Vérifier si le résultat est un dictionnaire d'erreur
            if isinstance(result, dict) and not result.get('success', True):
                context = self.get_context_data(invoice_id=invoice_id)
                context['error'] = result.get('error')
                return render(request, self.template_name, context)

            context = self.get_context_data(invoice_id=invoice_id)
            context['success'] = 'Paiement enregistré avec succès'
            return render(request, self.template_name, context)
        except ValueError as e:
            # Capturer les erreurs de validation du repository
            context = self.get_context_data(invoice_id=invoice_id)
            context['error'] = str(e)
            return render(request, self.template_name, context)
        except Exception as e:
            context = self.get_context_data(invoice_id=invoice_id)
            context['error'] = f'Erreur lors de l\'enregistrement : {str(e)}'
            return render(request, self.template_name, context)


class PaymentDeleteView(TemplateView):

    def post(self, request, payment_id, *args, **kwargs):
        invoice_id = request.POST.get('invoice_id')
        payment_service = PaymentService()
        try:
            payment_service.delete_payment(payment_id)
            # Rediriger vers la page de paiement avec l'invoice_id
            return redirect(f"{reverse('payment:payment')}?invoice_id={invoice_id}")
        except Exception as e:
            return render(request, 'payment/payment.html', {
                'error': f'Erreur lors de la suppression : {str(e)}',
                'invoice_id': invoice_id
            })



class PaymentUpdateView(TemplateView):
    template_name = 'payment/payment.html'

    def get_context_data(self, payment_id, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_service = PaymentService()

        try:
            payment = payment_service.get_payment_by_id(payment_id)
            context['payment'] = payment
            context['invoice_id'] = payment.invoice_id.invoice_id
        except Exception as e:
            context['payment'] = None
            context['invoice_id'] = None
            context['error'] = f'Erreur lors de la récupération du paiement : {str(e)}'

        return context

    def post(self, request, payment_id, *args, **kwargs):
        payment_method = request.POST.get('payment_method')
        state_payment = request.POST.get('state_payment')
        invoice_id = request.POST.get('invoice_id')
        amount = request.POST.get('amount')

        payment_service = PaymentService()
        try:
            # Vérifier champs remplis
            if not all([payment_method, state_payment, invoice_id, amount]):
                context = self.get_context_data(payment_id)
                context['error'] = 'Tous les champs sont obligatoires'
                return render(request, self.template_name, context)

            # Convertir amount
            try:
                amount = float(amount)
            except ValueError:
                context = self.get_context_data(payment_id)
                context['error'] = 'Le montant doit être un nombre valide'
                return render(request, self.template_name, context)

            payment_service.update_payment(payment_id, payment_method, state_payment, invoice_id, amount)
            # Rediriger vers page des paiements de la facture
            return redirect(f"{reverse('payment:payment')}?invoice_id={invoice_id}")
        except ValueError as e:
            # Capturer les erreurs de validation du repository
            context = self.get_context_data(payment_id)
            context['error'] = str(e)
            return render(request, self.template_name, context)
        except Exception as e:
            context = self.get_context_data(payment_id)
            context['error'] = f'Erreur lors de la modification : {str(e)}'
            return render(request, self.template_name, context)


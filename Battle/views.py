from .models import
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'TableBattleTest.html'
    def get_context_data(self, **kwargs):
        # Llamamos al metodo de la clase base
        context = super().get_context_data(**kwargs)
        # Agregamos los datos que queremos al contexto
        context['Jugadores'] =
        context['cartas_mano'] =
        context['cartas_descartes'] =
        context['cartas_reserva'] =
        context['cartas_activa'] =
        return context
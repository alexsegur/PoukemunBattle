from django.shortcuts import render
from Core.models import JugadorEntrenador,Mazo
from .models import JugadorBatalla,Batalla
from .admin import BatallaJugadorAdmin
from .models import
from django.views.generic.base import TemplateView


class SelectJugadorMazoView(TemplateView):
    template_name = 'selectTest.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jugadores'] = JugadorEntrenador.objects.all()
        context['mazos'] = Mazo.objectos.all()
        return context

    def post_create_battle(self, request, *args, **kwargs):
        jugador1_id = request.POST.get('jugador1')
        jugador2_id = request.POST.get('jugador2')
        mazo1_id = request.POST.get('mazo1')
        mazo2_id = request.POST.get('mazo2')

        batalla = Batalla.objects.create()
        batalla.definirnombre()
        JugadorBatalla.objects.create(jugador=jugador1_id, mazo=mazo1_id, batalla=batalla.id)
        JugadorBatalla.objects.create(jugador=jugador2_id, mazo=mazo2_id, batalla=batalla.id)



        # Redirige o realiza otra acción según lo necesites
        return redirect('TableBattleTest.html')


#class IndexView(TemplateView):
#    template_name = 'TableBattleTest.html'
#    def get_context_data(self, **kwargs):
#        # Llamamos al metodo de la clase base
#        context = super().get_context_data(**kwargs)
#        # Agregamos los datos que queremos al contexto
#        context['Jugadores'] =
#        context['cartas_mano'] =
#        context['cartas_descartes'] =
#        context['cartas_reserva'] =
#        context['cartas_activa'] =
#        return context
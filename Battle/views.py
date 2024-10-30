from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from Battle.models import CartaReservaJugador, CartaDescartesJugador, CartaMazoJugador, CartaManoJugador,Turno, TurnoJugador,Batalla, CartaActivaJugador, ReservaJugador, DescartesJugador, MazoJugador, ManoJugador,JugadorBatalla
from Battle.forms import GetPlayersForm, GetActionForm


class MostrarBatallaView(TemplateView):
    template_name = 'TableBattleTest.html'

    def get(self, request, *args, **kwargs):
        form = GetActionForm
        context = self.get_context_data()

        return self.render_to_response({'form': form})

    def get_context_data(self, request, *args, **kwargs):
        # Obtener la batalla
        context= super().get_context_data(**kwargs)
        batalla = get_object_or_404(Batalla, id=context['batalla'])

        # Obtener los jugadores y sus datos
        jugadores_batalla = JugadorBatalla.objects.filter(batalla=batalla).all()

        jugador_1 = jugadores_batalla[0]
        jugador_2 = jugadores_batalla[1]

        #Turno y TurnoJugador
        turno = Turno.objects.filter(batalla=batalla).lastest('turno')
        turnojugador_1 = TurnoJugador.objects.filter(turno=turno,jugadorbatalla = jugador_1).first()
        turnojugador_2 = TurnoJugador.objects.filter(turno=turno,jugadorbatalla = jugador_2).first()

        #TODO:Optimizar Datos de Jugador1 y Jugador2 con iteración

        # Datos del Jugador 1
        carta_activa_jugador_1 = CartaActivaJugador.objects.filter(batalla=batalla,jugador=jugador_1,turno=turnojugador_1).all()
        reserva_jugador_1 = ReservaJugador.objects.filter(batalla=batalla,jugador=jugador_1,turno=turnojugador_1).first()
        descartes_jugador_1 = DescartesJugador.objects.filter(batalla=batalla,jugador=jugador_1,turno=turnojugador_1).first()
        mazo_jugador_1 = MazoJugador.objects.filter(batalla=batalla,jugador=jugador_1,turno=turnojugador_1).first()
        mano_jugador_1 = ManoJugador.objects.filter(batalla=batalla,jugador=jugador_1,turno=turnojugador_1).first()

        carta_reserva_jugador_1 = CartaReservaJugador.objects.filter(reserva=reserva_jugador_1).all()
        carta_descartes_jugador_1 = CartaDescartesJugador.objects.filter(descartes=descartes_jugador_1).all()
        carta_mazo_jugador_1 = CartaMazoJugador.objects.filter(mazo=mazo_jugador_1).all()
        carta_mano_jugador_1 = CartaManoJugador.objects.filter(mano=mano_jugador_1).all()

        # Datos del Jugador 2
        carta_activa_jugador_2 = CartaActivaJugador.objects.filter(batalla=batalla,jugador=jugador_2,turno=turnojugador_2).all()
        reserva_jugador_2 = ReservaJugador.objects.filter(batalla=batalla,jugador=jugador_2,turno=turnojugador_2).first()
        descartes_jugador_2 = DescartesJugador.objects.filter(batalla=batalla,jugador=jugador_2,turno=turnojugador_2).first()
        mazo_jugador_2 = MazoJugador.objects.filter(batalla=batalla,jugador=jugador_2,turno=turnojugador_2).first()
        mano_jugador_2 = ManoJugador.objects.filter(batalla=batalla,jugador=jugador_2,turno=turnojugador_2).first()

        carta_reserva_jugador_2 = CartaReservaJugador.objects.filter(reserva=reserva_jugador_2).all()
        carta_descartes_jugador_2 = CartaDescartesJugador.objects.filter(descartes=descartes_jugador_2).all()
        carta_mazo_jugador_2 = CartaMazoJugador.objects.filter(mazo=mazo_jugador_2).all()
        carta_mano_jugador_2 = CartaManoJugador.objects.filter(mano=mano_jugador_2).all()

        # Pasar todos los datos al contexto
        context = {
            'batalla': batalla,
            'jugador_1': jugador_1,
            'carta_activa_jugador_1': carta_activa_jugador_1,
            'carta_reserva_jugador_1': carta_reserva_jugador_1,
            'carta_descartes_jugador_1': carta_descartes_jugador_1,
            'carta_mazo_jugador_1': carta_mazo_jugador_1,
            'carta_mano_jugador_1': carta_mano_jugador_1,
            'jugador_2': jugador_2,
            'carta_activa_jugador_2': carta_activa_jugador_2,
            'carta_reserva_jugador_2': carta_reserva_jugador_2,
            'carta_descartes_jugador_2': carta_descartes_jugador_2,
            'carta_mazo_jugador_2': carta_mazo_jugador_2,
            'carta_mano_jugador_2': carta_mano_jugador_2,
        }

        return context

    def post(self, request, *args, **kwargs):

        #accion
        pass

class CrearBatallaView(TemplateView):
    template_name = 'selectTest.html'

    def get(self, request, *args, **kwargs):
        form = GetPlayersForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = GetPlayersForm(request.POST)
        if form.is_valid():
            jugador_1 = form.cleaned_data['jugador_1']
            jugador_2 = form.cleaned_data['jugador_2']
            mazo_1 = form.cleaned_data['mazo_1']
            mazo_2 = form.cleaned_data['mazo_2']
            batalla,jugadoresbatalla = Batalla.iniciar_batalla(jugador_1,jugador_2,mazo_1,mazo_2)

            context = {
                'batalla': batalla,
                'jugadoresbatalla': jugadoresbatalla
            }

            return render(request, 'TableBattleTest.html', context=context)

        return self.render_to_response({'form': form})

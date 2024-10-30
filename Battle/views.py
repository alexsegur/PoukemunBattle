from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from Battle.models import CartaReservaJugador, CartaDescartesJugador, CartaMazoJugador, CartaManoJugador, Turno, \
    TurnoJugador, Batalla, CartaActivaJugador, ReservaJugador, DescartesJugador, MazoJugador, ManoJugador, \
    JugadorBatalla
from django.urls import reverse
from Battle.forms import GetPlayersForm, GetActionForm, GetDecksForm
from Core.models import JugadorEntrenador, Mazo


class MostrarBatallaView(TemplateView):
    template_name = 'TableBattleTest.html'

    def get(self, request, *args, **kwargs):
        form = GetActionForm
        context = self.get_context_data()

        return self.render_to_response({'form': form})

    def get_context_data(self, request, *args, **kwargs):
        # Obtener la batalla
        context = super().get_context_data(**kwargs)
        batalla = get_object_or_404(Batalla, id=context['batalla'])

        # Obtener los jugadores y sus datos
        jugadores_batalla = JugadorBatalla.objects.filter(batalla=batalla).all()

        jugador_1 = jugadores_batalla[0]
        jugador_2 = jugadores_batalla[1]

        # Turno y TurnoJugador
        turno = Turno.objects.filter(batalla=batalla).lastest('turno')
        turnojugador_1 = TurnoJugador.objects.filter(turno=turno, jugadorbatalla=jugador_1).first()
        turnojugador_2 = TurnoJugador.objects.filter(turno=turno, jugadorbatalla=jugador_2).first()

        # TODO:Optimizar Datos de Jugador1 y Jugador2 con iteración

        # Datos del Jugador 1
        carta_activa_jugador_1 = CartaActivaJugador.objects.filter(batalla=batalla, jugador=jugador_1,
                                                                   turno=turnojugador_1).all()
        reserva_jugador_1 = ReservaJugador.objects.filter(batalla=batalla, jugador=jugador_1,
                                                          turno=turnojugador_1).first()
        descartes_jugador_1 = DescartesJugador.objects.filter(batalla=batalla, jugador=jugador_1,
                                                              turno=turnojugador_1).first()
        mazo_jugador_1 = MazoJugador.objects.filter(batalla=batalla, jugador=jugador_1, turno=turnojugador_1).first()
        mano_jugador_1 = ManoJugador.objects.filter(batalla=batalla, jugador=jugador_1, turno=turnojugador_1).first()

        carta_reserva_jugador_1 = CartaReservaJugador.objects.filter(reserva=reserva_jugador_1).all()
        carta_descartes_jugador_1 = CartaDescartesJugador.objects.filter(descartes=descartes_jugador_1).all()
        carta_mazo_jugador_1 = CartaMazoJugador.objects.filter(mazo=mazo_jugador_1).all()
        carta_mano_jugador_1 = CartaManoJugador.objects.filter(mano=mano_jugador_1).all()

        # Datos del Jugador 2
        carta_activa_jugador_2 = CartaActivaJugador.objects.filter(batalla=batalla, jugador=jugador_2,
                                                                   turno=turnojugador_2).all()
        reserva_jugador_2 = ReservaJugador.objects.filter(batalla=batalla, jugador=jugador_2,
                                                          turno=turnojugador_2).first()
        descartes_jugador_2 = DescartesJugador.objects.filter(batalla=batalla, jugador=jugador_2,
                                                              turno=turnojugador_2).first()
        mazo_jugador_2 = MazoJugador.objects.filter(batalla=batalla, jugador=jugador_2, turno=turnojugador_2).first()
        mano_jugador_2 = ManoJugador.objects.filter(batalla=batalla, jugador=jugador_2, turno=turnojugador_2).first()

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
        # accion
        pass


class SeleccionarJugadorView(TemplateView):
    template_name = 'selectPlayers.html'

    def get(self, request, *args, **kwargs):
        form = GetPlayersForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = GetPlayersForm(request.POST)

        if form.is_valid():
            jugador1 = form.cleaned_data['jugador_1']
            jugador2 = form.cleaned_data['jugador_2']
            return redirect(reverse('select_mazos') + f'?jugador_1={jugador1.id}&jugador_2={jugador2.id}')

        return self.render_to_response({'form': form})


class SeleccionarMazoJugadorView(TemplateView):
    template_name = 'selectDecks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jugador_1_id = self.request.GET.get('jugador_1')
        jugador_2_id = self.request.GET.get('jugador_2')

        jugador_1 = JugadorEntrenador.objects.filter(id=jugador_1_id).first()
        jugador_2 = JugadorEntrenador.objects.filter(id=jugador_2_id).first()

        form = GetDecksForm(jugador_1=jugador_1, jugador_2=jugador_2)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        jugador_1_id = request.GET.get('jugador_1')
        jugador_2_id = request.GET.get('jugador_2')

        # Obtener instancias de los jugadores
        jugador_1 = JugadorEntrenador.objects.filter(id=jugador_1_id).first()
        jugador_2 = JugadorEntrenador.objects.filter(id=jugador_2_id).first()

        form = GetDecksForm(request.POST, jugador_1=jugador_1, jugador_2=jugador_2)

        if form.is_valid():
            mazo_1 = form.cleaned_data['mazo_jugador_1']
            mazo_2 = form.cleaned_data['mazo_jugador_2']
            return redirect(reverse('mostrar_batalla') + f'?jugador_1={jugador_1.id}&jugador_2={jugador_2.id}&mazo_1={mazo_1.id}&mazo_2={mazo_2.id}')

        return self.render_to_response({'form': form})

class InicioDeBatallaView(TemplateView):
    template_name = 'startBattleTable.html'

    def post(self, request, *args, **kwargs):
        jugador_1_id = self.request.GET.get('jugador_1')
        jugador_2_id = self.request.GET.get('jugador_2')
        mazo_1_id = self.request.GET.get('mazo_1')
        mazo_2_id = self.request.GET.get('mazo_2')

        jugador_1 = JugadorEntrenador.objects.filter(id=jugador_1_id).first()
        jugador_2 = JugadorEntrenador.objects.filter(id=jugador_2_id).first()
        mazo_1 = Mazo.objects.filter(id=mazo_1_id).first()
        mazo_2 = Mazo.objects.filter(id=mazo_2_id).first()

        batalla,jugadoresbatalla = Batalla.iniciar_batalla(jugador_1,jugador_2,mazo_1,mazo_2)







    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jugador_1_id = self.request.GET.get('jugador_1')
        jugador_2_id = self.request.GET.get('jugador_2')
        mazo_1_id = self.request.GET.get('mazo_1')
        mazo_2_id = self.request.GET.get('mazo_2')

        jugador_1 = JugadorEntrenador.objects.filter(id=jugador_1_id).first()
        jugador_2 = JugadorEntrenador.objects.filter(id=jugador_2_id).first()
        mazo_1 = Mazo.objects.filter(id=mazo_1_id).first()
        mazo_2 = Mazo.objects.filter(id=mazo_2_id).first()

        context['jugador_1'] = ""
        return context


from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from Battle.models import CartaReservaJugador, CartaDescartesJugador, CartaMazoJugador, CartaManoJugador, Turno, \
    TurnoJugador, Batalla, CartaActivaJugador, ReservaJugador, DescartesJugador, MazoJugador, ManoJugador, \
    JugadorBatalla
from django.urls import reverse
from Battle.forms import GetPlayersForm, GetActionForm, GetDecksForm
from Core.models import JugadorEntrenador, Mazo


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
            batalla, _ = Batalla.iniciar_batalla(jugador_1, jugador_2, mazo_1, mazo_2)
            return redirect(reverse('mostrar_batalla') + f'?batalla={batalla.id}&jugador_1={jugador_1.id}&jugador_2={jugador_2.id}&mazo_1={mazo_1.id}&mazo_2={mazo_2.id}')

        return self.render_to_response({'form': form})


class InicioDeBatallaView(TemplateView):
    template_name = 'TableBattleTest.html'

    def post(self, request, *args, **kwargs):
        # Obtiene los parámetros de la URL
        jugador_1_id = request.POST.get('jugador_1')
        jugador_2_id = request.POST.get('jugador_2')
        mazo_1_id = request.POST.get('mazo_1')
        mazo_2_id = request.POST.get('mazo_2')
        batalla_id = request.POST.get('batalla')

        # Consulta para obtener los jugadores y mazos
        jugador_1 = JugadorEntrenador.objects.filter(id=jugador_1_id).first()
        jugador_2 = JugadorEntrenador.objects.filter(id=jugador_2_id).first()
        mazo_1 = Mazo.objects.filter(id=mazo_1_id).first()
        mazo_2 = Mazo.objects.filter(id=mazo_2_id).first()
        batalla = Batalla.objects.filter(id=batalla_id).first


        if batalla is not None:
            # Genera el contexto y renderiza el template con los datos de la batalla
            context = self.get_context_data()
            return render(request, self.template_name, context)
        else:
            # Mensaje de error si no se pudo iniciar la batalla
            return render(request, self.template_name, {'error': 'No se pudo iniciar la batalla'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        batalla_id = self.request.POST.get('batalla')
        batalla = Batalla.objects.filter(id=batalla_id).first
        print(f'Esto son batalla_id y batalla en get_context():{batalla_id}, {batalla}')

        if batalla:
            # Obtener los jugadores de la batalla
            jugadores_batalla = JugadorBatalla.objects.filter(batalla=batalla_id).all()
            print(f'jugadores_batalla sale esto:{jugadores_batalla}, {type(jugadores_batalla)}')
            jugador_1 = jugadores_batalla[0]
            jugador_2 = jugadores_batalla[1]

            # Obtener el último turno y los datos correspondientes a los jugadores
            turno = Turno.objects.filter(batalla=batalla).latest('turno')
            turnojugador_1 = TurnoJugador.objects.filter(turno=turno, jugadorbatalla=jugador_1).first()
            turnojugador_2 = TurnoJugador.objects.filter(turno=turno, jugadorbatalla=jugador_2).first()

            # Datos del Jugador 1
            carta_activa_jugador_1 = CartaActivaJugador.objects.filter(batalla=batalla, jugador=jugador_1, turno=turnojugador_1).all()
            reserva_jugador_1 = ReservaJugador.objects.filter(batalla=batalla, jugador=jugador_1, turno=turnojugador_1).first()
            descartes_jugador_1 = DescartesJugador.objects.filter(batalla=batalla, jugador=jugador_1, turno=turnojugador_1).first()
            mazo_jugador_1 = MazoJugador.objects.filter(batalla=batalla, jugador=jugador_1, turno=turnojugador_1).first()
            mano_jugador_1 = ManoJugador.objects.filter(batalla=batalla, jugador=jugador_1, turno=turnojugador_1).first()

            carta_reserva_jugador_1 = CartaReservaJugador.objects.filter(reserva=reserva_jugador_1).all()
            carta_descartes_jugador_1 = CartaDescartesJugador.objects.filter(descartes=descartes_jugador_1).all()
            carta_mazo_jugador_1 = CartaMazoJugador.objects.filter(mazo=mazo_jugador_1).all()
            carta_mano_jugador_1 = CartaManoJugador.objects.filter(mano=mano_jugador_1).all()

            # Datos del Jugador 2
            carta_activa_jugador_2 = CartaActivaJugador.objects.filter(batalla=batalla, jugador=jugador_2, turno=turnojugador_2).all()
            reserva_jugador_2 = ReservaJugador.objects.filter(batalla=batalla, jugador=jugador_2, turno=turnojugador_2).first()
            descartes_jugador_2 = DescartesJugador.objects.filter(batalla=batalla, jugador=jugador_2, turno=turnojugador_2).first()
            mazo_jugador_2 = MazoJugador.objects.filter(batalla=batalla, jugador=jugador_2, turno=turnojugador_2).first()
            mano_jugador_2 = ManoJugador.objects.filter(batalla=batalla, jugador=jugador_2, turno=turnojugador_2).first()

            carta_reserva_jugador_2 = CartaReservaJugador.objects.filter(reserva=reserva_jugador_2).all()
            carta_descartes_jugador_2 = CartaDescartesJugador.objects.filter(descartes=descartes_jugador_2).all()
            carta_mazo_jugador_2 = CartaMazoJugador.objects.filter(mazo=mazo_jugador_2).all()
            carta_mano_jugador_2 = CartaManoJugador.objects.filter(mano=mano_jugador_2).all()

            # Agregar datos al contexto
            context.update({
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
            })

        return context
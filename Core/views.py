import json

from django.http import JsonResponse
from Core.models import CartaPokemon, BoosterPack, Coleccion
from django.views.generic.base import TemplateView
from Core.forms import BoosterPackForm


class IndexView(TemplateView):
    template_name = 'pokemon_list.html'

    def get(self, request, *args, **kwargs):
        form = BoosterPackForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = BoosterPackForm(request.POST)

        if form.is_valid():
            entrenador = form.cleaned_data['entrenador']
            booster_pack = BoosterPack.objects.first()
            cartas_obtenidas = booster_pack.open_booster()

            for carta in cartas_obtenidas:
                Coleccion.asignar_carta_al_entrenador(entrenador, carta)

            ultimas_cartas = Coleccion.objects.filter(entrenador=entrenador).order_by('-id')[:5]

            context = self.get_context_data()
            context.update({
                'form': form,
                'cartas_obtenidas': ultimas_cartas,
                'entrenador': entrenador
            })

            return self.render_to_response(context)

        return self.render_to_response({'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pokemons'] = CartaPokemon.objects.all()
        return context


class CollectionCardsView(TemplateView):
    template_name = 'colection_cards_repeat.html'

    def cards_repeated(self):
        collections = Coleccion.objects.select_related('entrenador').all()

        resultado = {}

        for collection in collections:
            entrenador = collection.entrenador
            carta = collection.pokemon

            if entrenador not in resultado:
                resultado[entrenador] = {}

            if carta in resultado[entrenador]:
                resultado[entrenador][carta] += 1
            else:
                resultado[entrenador][carta] = 1

        players = [
            {'nombre': entrenador.nombre,
                'cartas': [{'carta': carta.nombre_pokemon, 'cantidad': cantidad} for carta, cantidad in cartas.items()]}
            for entrenador, cartas in resultado.items()
        ]

        return json.dumps(players)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_by_player'] = self.cards_repeated()
        return context

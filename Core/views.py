import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from Core.models import CartaPokemon, BoosterPack, Coleccion,JugadorEntrenador
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

class CompareCollectionToTotalView(TemplateView):
    template_name = 'compare_collection_to_total.html'
    def repeated_compared_to_total(self):
        id_entrenador = self.request.GET.get('id_entrenador')

        # Si se proporciona id_entrenador, obtener el entrenador específico
        entrenador = None
        if id_entrenador:
            entrenador = get_object_or_404(JugadorEntrenador, id=id_entrenador)

        collections = Coleccion.objects.select_related('entrenador').all()
        resultado = {}
        total_cartas = {}

        # Procesar cada colección para agrupar las cartas por entrenador y total
        for collection in collections:
            entrenador_obj = collection.entrenador
            carta = collection.pokemon

            # Para la colección del entrenador específico
            if entrenador and entrenador_obj == entrenador:
                if carta in resultado:
                    resultado[carta] += 1
                else:
                    resultado[carta] = 1

            # Para el total de cartas en todas las colecciones
            if carta in total_cartas:
                total_cartas[carta] += 1
            else:
                total_cartas[carta] = 1

        # Formatear los datos en una lista de listas para Google Charts
        chart_data = [["Pokemon", "Cantidad Entrenador", "Cantidad Total"]]
        for carta, total_count in total_cartas.items():
            entrenador_count = resultado.get(carta, 0)  # Obtiene la cantidad en el entrenador o 0 si no existe
            chart_data.append([carta.nombre_pokemon, entrenador_count, total_count])

        return chart_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_entrenador = self.request.GET.get('id_entrenador')
        entrenador = None
        if id_entrenador:
            entrenador = get_object_or_404(JugadorEntrenador, id=id_entrenador)

        context['chart_data'] = self.repeated_compared_to_total()
        context['entrenador'] = entrenador
        return context
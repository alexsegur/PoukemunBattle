import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from Core.models import CartaPokemon, BoosterPack, Coleccion,JugadorEntrenador
from django.views.generic.base import TemplateView
from Core.forms import PickEntrenadorForm



class IndexView(TemplateView):
    template_name = 'pokemon_list.html'

    def get(self, request, *args, **kwargs):
        form = PickEntrenadorForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = PickEntrenadorForm(request.POST)

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

    def get(self, request, *args, **kwargs):
        form = PickEntrenadorForm()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = PickEntrenadorForm(request.POST)
        if form.is_valid():
            entrenador = form.cleaned_data['entrenador']

            json_comparison = self.join_cards_entrenador_y_total(entrenador)
            context = {
                'form': form,
                'json_comparison': json_comparison,
                'entrenador': entrenador
            }
            return self.render_to_response(context)
        else:
            # En caso de error, vuelve a mostrar el formulario
            context = {'form': form}
            return self.render_to_response(context)


    def cards_repeated_en_entrenador(self,entrenadorjugador):

        entrenador = get_object_or_404(JugadorEntrenador, id=entrenadorjugador.id)
        collections = Coleccion.objects.select_related('entrenador').all()
        resultado = {}

        for collection in collections:
            entrenador_obj = collection.entrenador
            carta = collection.pokemon

            if entrenador and entrenador_obj == entrenador:
                if entrenador not in resultado:
                    resultado[entrenador] = {}

                if carta in resultado[entrenador]:
                    resultado[entrenador][carta] += 1
                else:
                    resultado[entrenador][carta] = 1

        comparison = [
            {'nombre': entrenador.nombre,
                'cartas': [{'carta': carta.nombre_pokemon, 'cantidad': cantidad} for carta, cantidad in cartas.items()]}
            for entrenador, cartas in resultado.items()
        ]
        return comparison
    def total_cards_repeated(self):
        collections = Coleccion.objects.all()
        total_cartas = {}

        for collection in collections:
            carta = collection.pokemon
            entrenador = 'total'

            # Para el total de cartas en todas las colecciones
            if entrenador not in total_cartas:
                total_cartas[entrenador]={}

            if carta in total_cartas[entrenador]:
                total_cartas[entrenador][carta] += 1
            else:
                total_cartas[entrenador][carta] = 1

        total = [
            {'nombre': entrenador,
             'cartas': [{'carta': carta.nombre_pokemon, 'cantidad': cantidad} for carta, cantidad in cartas.items()]}
            for entrenador, cartas in total_cartas.items()
        ]
        return total

    def join_cards_entrenador_y_total(self,id_entrenador):


        # Obtener las cartas del entrenador especificado y las cartas totales
        comparison = self.cards_repeated_en_entrenador(id_entrenador)
        total = self.total_cards_repeated()

        if total:
            comparison.append(total[0])

        return json.dumps(comparison)


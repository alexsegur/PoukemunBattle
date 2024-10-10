from .models import CartaPokemon
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'pokemon_list.html'
    def get_context_data(self, **kwargs):
        # Llamamos al metodo de la clase base
        context = super().get_context_data(**kwargs)
        # Agregamos los datos que queremos al contexto
        context['pokemons'] = CartaPokemon.objects.all()
        return context
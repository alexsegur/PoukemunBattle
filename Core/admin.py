from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import CartaPokemon, Ataque, CartaPokemonAtaque, JugadorEntrenador, Coleccion, Mazo, CartaMazo


class PokemonAtaqueInline(admin.TabularInline):
    model = CartaPokemonAtaque
    extra = 1
    max_num = 20 #Un pokemon solo puede llegar a aprender hasta (max_num) ataques
    fields = ('ataque',)


class ColeccionInlineForm(forms.ModelForm):

    class Meta:
        model = Coleccion
        fields = ['pokemon', 'ataque1', 'ataque2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'pokemon' in self.data:
            try:
                pokemon_id = int(self.data.get('pokemon'))
                # Filtrar los ataques que están relacionados con el Pokémon seleccionado
                self.fields['ataque1'].queryset = CartaPokemonAtaque.objects.filter(pokemon_id=pokemon_id)
                self.fields['ataque2'].queryset = CartaPokemonAtaque.objects.filter(pokemon_id=pokemon_id)
            except (ValueError, TypeError):
                pass  # Manejar el caso en el que aún no haya un Pokémon seleccionado
        elif self.instance.pk:
            # Filtrar cuando se está editando una instancia existente
            self.fields['ataque1'].queryset = self.instance.pokemon.ataques_aprendibles.all()
            self.fields['ataque2'].queryset = self.instance.pokemon.ataques_aprendibles.all()

    def clean(self):
        cleaned_data = super().clean()
        ataque1 = cleaned_data.get("ataque1")
        ataque2 = cleaned_data.get("ataque2")

        # Verificar si ambos ataques son iguales
        if ataque1 == ataque2:
            raise ValidationError("No puedes seleccionar el mismo ataque dos veces.")

        return cleaned_data

class ColeccionInline(admin.TabularInline):
    model = Coleccion
    form = ColeccionInlineForm
    extra = 0

class CartaMazoInline(admin.TabularInline):
    model = CartaMazo
    extra = 1
    max_num = 10

class MazoInline(admin.TabularInline):
    model = Mazo
    extra = 0


@admin.register(Mazo)
class MazoAdmin(admin.ModelAdmin):
    model = Mazo
    extra = 1
    max_num = 4
    inlines = [CartaMazoInline]


class PokemonAdmin(admin.ModelAdmin):
    list_display = ('nombre_pokemon','id',)
    inlines = [PokemonAtaqueInline]

@admin.register(JugadorEntrenador)
class JugadorEntrenadorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    inlines = [ColeccionInline, MazoInline]

admin.site.register(Ataque)
admin.site.register(CartaPokemon, PokemonAdmin)



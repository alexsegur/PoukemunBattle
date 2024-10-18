import random

from django.db import models


class Ataque(models.Model):
    nombre = models.CharField(max_length=50, default='')
    damage = models.PositiveIntegerField(default=0)
    coste = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre


class Set(models.Model):
    name = models.CharField(max_length=50, default='', null=False, blank=False)

    def __str__(self):
        return self.name


class CartaPokemon(models.Model):  # Intermedia lvl1
    nombre_pokemon = models.CharField(max_length=50, default='')
    salud_max = models.IntegerField(default=0)
    energia = models.IntegerField(default=0)
    rare = models.BooleanField(default=False)
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='set_de_la_carta', null=True)

    def __str__(self):
        return self.nombre_pokemon


class CartaPokemonAtaque(models.Model):  # Intermedia lvl1
    pokemon = models.ForeignKey(CartaPokemon, on_delete=models.CASCADE, related_name='ataques_aprendibles')
    ataque = models.ForeignKey(Ataque, on_delete=models.CASCADE)

    # Lista todos los ataques que puede aprender un pokemon

    def __str__(self):
        return '{ataque}'.format(pokemon=self.pokemon, ataque=self.ataque)


class JugadorEntrenador(models.Model):
    nombre = models.CharField(default='', max_length=50)

    def __str__(self):
        return self.nombre


class Coleccion(models.Model):  # Tabla intermedia lvl2 Entrenador - CartaPokemonAtaque
    entrenador = models.ForeignKey(JugadorEntrenador, related_name='coleccion_entrenador', on_delete=models.CASCADE)
    pokemon = models.ForeignKey(CartaPokemon, on_delete=models.CASCADE, related_name='pokemons_coleccionados')
    ataque1 = models.ForeignKey(CartaPokemonAtaque, on_delete=models.CASCADE, related_name='ataque_debil', null=True)
    ataque2 = models.ForeignKey(CartaPokemonAtaque, on_delete=models.CASCADE, related_name='ataque_fuerte', null=True)

    def __str__(self):
        return '{entrenador}, {pokemon}'.format(entrenador=self.entrenador, pokemon=self.pokemon)

    @classmethod
    def asignar_carta_al_entrenador(cls, entrenador, carta):
        ataques_posibles = CartaPokemonAtaque.objects.filter(pokemon=carta)

        if ataques_posibles.exists():
            if ataques_posibles.count() == 1:
                ataque1 = random.choice(ataques_posibles)
                ataque2 = None
            else:
                ataque1 = random.choice(ataques_posibles)
                ataques_posibles=-ataque1
                ataque2 = random.choice(ataques_posibles)
        else:
            ataque1, ataque2 = None, None

        coleccion = cls.objects.create(
            entrenador=entrenador,
            pokemon=carta,
            ataque1=ataque1,
            ataque2=ataque2
        )
        return coleccion


class Mazo(models.Model):  # Tabla intermedia lvl1.5 Mazo - Entrenador
    entrenador = models.ForeignKey(JugadorEntrenador, on_delete=models.CASCADE, null=True)
    nombre_mazo = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre_mazo


class CartaMazo(models.Model):  # Tabla intermedia lvl2 Mazo - Coleccion
    carta = models.ForeignKey(Coleccion, on_delete=models.CASCADE, null=False)
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE, null=False)


class BoosterPack(models.Model):
    name = models.CharField(max_length=50, default='')
    price = models.PositiveIntegerField()
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='set_del_sobre', null=True)

    def open_booster(self):
        common_cards = CartaPokemon.objects.filter(set=self.set, rare=False)
        rare_cards = CartaPokemon.objects.filter(set=self.set, rare=True)

        selected_cards = []

        for _ in range(4):
            if random.random() < 0.02 and rare_cards.exists():
                card_selected = random.choice(rare_cards)
            else:
                card_selected = random.choice(common_cards)
            selected_cards.append(card_selected)

        if rare_cards.exists():
            rare_card_secure = random.choice(rare_cards)
            selected_cards.append(rare_card_secure)
        else:
            no_rare_cards_created = random.choice(common_cards)
            selected_cards.append(no_rare_cards_created)

        return selected_cards

    def __str__(self):
        return '{} - {}'.format(self.name, self.set)

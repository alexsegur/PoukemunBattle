from django.db import models


class Ataque(models.Model):
    nombre = models.CharField(max_length=50, default='')
    damage = models.PositiveIntegerField(default=0)
    coste = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{nombre}, {damage}, {coste}'.format(nombre=self.nombre, damage=self.damage, coste=self.coste)


class CartaPokemon(models.Model):  # Intermedia lvl1
    nombre_pokemon = models.CharField(max_length=50, default='')
    salud_max = models.IntegerField(default=0)
    energia = models.IntegerField(default=0)


    def __str__(self):
        return '{nombre_pokemon}, {salud_max}'.format(nombre_pokemon=self.nombre_pokemon, salud_max=self.salud_max)


class CartaPokemonAtaque(models.Model):  # Intermedia lvl1
    pokemon = models.ForeignKey(CartaPokemon, on_delete=models.CASCADE, related_name='ataques_aprendibles')
    ataque = models.ForeignKey(Ataque, on_delete=models.CASCADE)

    # Lista todos los ataques que puede aprender un pokemon

    def __str__(self):
        return '{pokemon}, {ataque}'.format(pokemon=self.pokemon, ataque=self.ataque)


class JugadorEntrenador(models.Model):
    nombre = models.CharField(default='', max_length=50)

    def __str__(self):
        return self.nombre


class Coleccion(models.Model):  # Tabla intermedia lvl2 Entrenador - CartaPokemonAtaque
    entrenador = models.ForeignKey(JugadorEntrenador, related_name='coleccion_entrenador', on_delete=models.CASCADE)
    pokemon = models.OneToOneField(CartaPokemon, on_delete=models.CASCADE, related_name='pokemons_coleccionados',
                                   primary_key=False)
    ataque1 = models.ForeignKey(CartaPokemonAtaque, on_delete=models.CASCADE, related_name='ataque_debil', null=True)
    ataque2 = models.ForeignKey(CartaPokemonAtaque, on_delete=models.CASCADE, related_name='ataque_fuerte', null=True)

    def __str__(self):
        return '{entrenador}, {pokemon}'.format(entrenador=self.entrenador, pokemon=self.pokemon)


class Mazo(models.Model):  # Tabla intermedia lvl1.5 Mazo - Entrenador
    entrenador = models.ForeignKey(JugadorEntrenador, on_delete=models.CASCADE, null=True)
    nombre_mazo = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre_mazo

class CartaMazo(models.Model): #Tabla intermedia lvl2 Mazo - Coleccion
    carta = models.ForeignKey(Coleccion, on_delete=models.CASCADE, null=False)
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE, null=False)

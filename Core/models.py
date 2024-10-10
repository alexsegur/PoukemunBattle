from django.db import models


class Ataque(models.Model):
    nombre = models.CharField(max_length=50, default='')
    damage = models.PositiveIntegerField(default=0)
    coste = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{nombre}, {damage}, {coste}'.format(nombre=self.nombre, damage=self.damage, coste=self.coste)


class CartaPokemon(models.Model): #Intermedia lvl1
    nombre_pokemon = models.CharField(max_length=50, default='')
    salud_max = models.IntegerField(default=0)
    energia= models.IntegerField(default = 0)

    #def clean(self):

    def __str__(self):
        return '{nombre_pokemon}, {salud_max}'.format(nombre_pokemon=self.nombre_pokemon, salud_max=self.salud_max)


class CartaPokemonAtaque(models.Model): #Intermedia lvl1
    pokemon = models.ForeignKey(CartaPokemon, on_delete=models.CASCADE, related_name='ataques_aprendibles')
    ataque = models.ForeignKey(Ataque, on_delete=models.CASCADE)
    # Lista todos los ataques que puede aprender un pokemon

    def __str__(self):
        return '{pokemon}, {ataque}'.format(pokemon=self.pokemon, ataque=self.ataque)

class JugadorEntrenador(models.Model):
    nombre = models.CharField(default='',max_length=50)

    def __str__(self):
        return self.nombre


class Coleccion(models.Model):  #Tabla intermedia lvl2 Entrenador - CartaPokemonAtaque
    entrenador = models.ForeignKey(JugadorEntrenador, related_name='coleccion_entrenador', on_delete=models.CASCADE)
    pokemon = models.OneToOneField(CartaPokemon, on_delete=models.CASCADE, related_name='pokemons_coleccionados' , primary_key=False)
    ataque1 = models.ForeignKey(CartaPokemonAtaque, on_delete=models.CASCADE, related_name='ataque_debil', null=True)
    ataque2 = models.ForeignKey(CartaPokemonAtaque, on_delete=models.CASCADE, related_name='ataque_fuerte', null=True)

    def __str__(self):
        return '{entrenador}, {pokemon}'.format(entrenador=self.entrenador, pokemon=self.pokemon)

class Mazo(models.Model):
    nombre = models.CharField(default='',max_length=50, unique=True)

class MazoEntrenador(models.Model): #Tabla intermedia lvl1 Entrenador - Mazo
    nombre = models.ForeignKey(Mazo, related_name='nombre_mazo', on_delete=models.CASCADE, null=True)
    entrenador = models.ForeignKey(JugadorEntrenador, related_name='entrenador_mazo', on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ['nombre', 'entrenador']

    def __str__(self):
        return '{entrenador},{nombre}'.format(entrenador=self.entrenador,nombre=self.nombre)

class MazoCartaPokemon(models.Model): #Tabla intermedia lvl2 MazoEntrenador - Colección
    mazo = models.ForeignKey(MazoEntrenador, related_name='entrenador_mazo', on_delete=models.CASCADE, null=True)
    pokemon = models.ForeignKey(Coleccion, related_name='pokemon_mazo',on_delete=models.CASCADE, null=True)
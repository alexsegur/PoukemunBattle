import random

from Core.models import JugadorEntrenador, CartaMazo, Mazo
from django.db.models import Q

from django.db import models


class Batalla(models.Model):
    nombre = models.CharField(default='', max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null= False)

    def __str__(self):
        return '{}_{}'.format(self.id,self.fecha)


class Turno(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('batalla', 'turno',)

class JugadorBatalla(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorEntrenador, on_delete=models.CASCADE)
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('batalla', 'jugador','mazo'),)

    def iniciar_batalla(self, jugador_1, jugador_2, mazo_1, mazo_2):
        jugador_batalla_1 = JugadorBatalla.objects.create(batalla=self, jugador=jugador_1, mazo=mazo_1)
        jugador_batalla_2 = JugadorBatalla.objects.create(batalla=self, jugador=jugador_2, mazo=mazo_2)

        # Arreglar esto
        jugador_batalla_1.robar_cartas(3)
        jugador_batalla_2.robar_cartas(3)


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)


class CartaManoJugador(models.Model):
    mano = models.ForeignKey(ManoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def robar_cartas(self, num_cartas):

        cartas_disponibles = CartaMazo.objects.all().exclude(
            id__in=self.CartaManoJugador_set.values_list('carta', flat=True)) #OR en Descartes OR Activa....
        cartas_a_robar = random.sample(list(cartas_disponibles), min(num_cartas, len(cartas_disponibles)))
        for carta in cartas_a_robar:
            CartaManoJugador.objects.create(mano=self, carta=carta)


class DescartesJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)


class CartaDescartesJugador(models.Model):
    descarte = models.ForeignKey(DescartesJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)


class ReservaJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)


class CartaReservaJugador(models.Model):
    reserva = models.ForeignKey(ReservaJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)


class AccionTurnoJugador(models.Model):
    ACCION = [
        ('1', 'Ataque'),
        ('2', 'Pasar turno'),
        ('3', 'Recarga energía'),
        ('4', 'Jugar carta'),
    ]
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    accion = models.CharField(max_length=50, choices=ACCION, null=True, blank=True)

    def realizar_accion(self, accion, objetivo=None):
        if accion == '1':
            self.atacar(objetivo)
        elif accion == '2':
            self.pasar_turno()
        elif accion == '3':
            self.recargar_energia()
        elif accion == '4':
            self.jugar_carta()


class TurnoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE, null=True)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    energia = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('turno', 'jugador')


class CartaActivaJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo,on_delete=models.CASCADE)

    def atacar(self,objetivo,ataque):


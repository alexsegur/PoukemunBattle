from Core.models import JugadorEntrenador, CartaMazo, Mazo

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

    # Si se quiere: limitar batallas a X jugadores.
    class Meta:
        unique_together = (('batalla', 'jugador','mazo'),)


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)


class CartaManoJugador(models.Model):
    mano = models.ForeignKey(ManoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)


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
    accion = models.CharField(max_length=50, choices=ACCION, null=True, blank=True)



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

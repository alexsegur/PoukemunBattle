from Core.models import JugadorEntrenador, CartaMazo, Mazo

from django.db import models


class Batalla(models.Model):
    nombre = models.CharField(default='')
    fecha = models.DateTimeField(auto_now_add=True)


# class MazoTurno : No se si tener físicamente el mazo o ir a buscar de forma random CartaMazo
class Turno(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.PositiveIntegerField(default=1)


class JugadorBatalla(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorEntrenador, on_delete=models.CASCADE)
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE)

    # Si se quiere: limitar batallas a X jugadores.
    class Meta:
        unique_together = ('batalla', 'jugador')
        unique_together2 = ('jugador', 'mazo')


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)
    # Si se quiere: Limitar las cartas en Mano a X Cartas


class DescartesJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)


class ReservaTurnoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)
    # Si se quiere: Limitar las cartas en Reserva a X Cartas


class AccionTurnoJugador(models.Model):
    ACCION = [
        ('1', 'Ataque'),
        ('2', 'Pasar turno'),
        ('3', 'Recarga energía'),
        ('4', 'Jugar carta'),
    ]
    accion = models.CharField(max_length=50, choices=ACCION, null=True, blank=True)


class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    activo = models.ForeignKey(CartaMazo, on_delete=models.CASCADE, null=True, blank=True)
    energia = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('turno', 'jugador')

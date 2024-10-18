import random
from Core.models import JugadorEntrenador, CartaMazo, Mazo
from django.db.models import Q

from django.db import models


class Batalla(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null= False)

    def save(self, *args, **kwargs):
        super(Batalla, self).save(*args, **kwargs)
        if not self.nombre:
            self.nombre = '{}_{}'.format(self.id, self.fecha)
            super(Batalla, self).save(*args, **kwargs)
    def __str__(self):
        return self.nombre


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

    def iniciar_batalla(self, batalla, jugador_1, jugador_2, mazo_1, mazo_2):
        jugador_batalla_1 = JugadorBatalla.objects.create(batalla=batalla, jugador=jugador_1, mazo=mazo_1)
        jugador_batalla_2 = JugadorBatalla.objects.create(batalla=batalla, jugador=jugador_2, mazo=mazo_2)

        llenar_mazo(jugador_batalla_1)
        llenar_mazo(jugador_batalla_2)

        jugador_batalla_1.robar_cartas(3,jugador_batalla_1,)
        jugador_batalla_2.robar_cartas(3)


class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugadorbatalla = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    energia = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('turno', 'jugadorbatalla')




class CartaMazoJugador(models.Model):
    mazojugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)


    def llenar_mazo(self, jugadorbatalla):

        cartas_en_mazo = CartaMazo.objects.filter(mazo=jugadorbatalla.mazo)
        for carta in cartas_en_mazo:
            CartaMazoJugador.objects.create(mazojugador=jugadorbatalla, carta=carta)


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)


class CartaManoJugador(models.Model):
    mano = models.ForeignKey(ManoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)


    def robar_cartas(self,jugadorbatalla, mano, num_cartas):

        cartas_disponibles = CartaMazoJugador.objects.filter(mazojugador=jugadorbatalla)
        cartas_a_robar = random.sample(list(cartas_disponibles), min(num_cartas, len(cartas_disponibles)))

        for carta in cartas_a_robar:
            CartaManoJugador.objects.create(mano=mano, carta=carta)
            CartaMazoJugador.objects.filter(mazojugador=jugadorbatalla).filter(carta=carta).first().delete()


    def jugar_carta(self,carta):
        carta_activa = CartaActivaJugador.objects.all()
        if carta_activa:

        CartaActivaJugador.objects.create(batalla= , turno= , jugador= ,carta=carta)
        CartaManoJugador.objects.filter(carta=carta).first().delete()


class CartaActivaJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo,on_delete=models.CASCADE)

    def atacar(self,objetivo,ataque):
        pass


class DescartesJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)



class CartaDescartesJugador(models.Model):
    descarte = models.ForeignKey(DescartesJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def carta_debilitada(self, carta, descarte):
        CartaDescartesJugador.objects.create(descarte=descarte,carta=carta)
        CartaActivaJugador.objets.filter(jugador=descarte.jugador).delete()


class ReservaJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)


class CartaReservaJugador(models.Model):
    reserva = models.ForeignKey(ReservaJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def rejugar_carta(self, carta, ):


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




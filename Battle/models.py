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

    def iniciar_batalla(self, jugador_1, jugador_2, mazo_1, mazo_2):
        batalla1 = Batalla.create()
        batalla1.save()

        jugador_batalla_1 = JugadorBatalla.objects.create(batalla=batalla1, jugador=jugador_1, mazo=mazo_1)
        jugador_batalla_2 = JugadorBatalla.objects.create(batalla=batalla1, jugador=jugador_2, mazo=mazo_2)
        jugador_batalla_1.save()
        jugador_batalla_2.save()

        turno = Turno.create(batalla=batalla, turno=1)
        turno.save()

        turnojugador1 = TurnoJugador.create(turno=turno,jugadorbatalla=jugador_batalla_1)
        turnojugador2 = TurnoJugador.create(turno=turno, jugadorbatalla=jugador_batalla_2)




        llenar_mazo(jugador_batalla_1)
        llenar_mazo(jugador_batalla_2)

        robar_cartas(3,jugador_batalla_1,)
        robar_cartas(3)


class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugadorbatalla = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    energia = models.PositiveIntegerField(default=0) #pasar a batalla

    class Meta:
        unique_together = ('turno', 'jugadorbatalla')

    def robar_carta(self):
        pass

class MazoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

class CartaMazoJugador(models.Model):
    mazojugador = models.ForeignKey(MazoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)


    def llenar_mazo(self, jugadorbatalla):
        mazojugador = MazoJugador.objects.filter(jugador=jugadorbatalla)
        cartas_en_mazo = CartaMazo.objects.filter(mazo=mazojugador.jugador.mazo)
        for carta in cartas_en_mazo:
            CartaMazoJugador.objects.create(mazojugador=mazojugador, carta=carta)


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def definir_mazo(self):



class CartaManoJugador(models.Model):
    mano = models.ForeignKey(ManoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)


    def robar_cartas(self,jugadorbatalla, mano, num_cartas):

        cartas_disponibles = CartaMazoJugador.objects.filter(mazojugador=jugadorbatalla)
        cartas_a_robar = random.sample(list(cartas_disponibles), min(num_cartas, len(cartas_disponibles)))

        for carta in cartas_a_robar:
            CartaManoJugador.objects.create(mano=mano, carta=carta)
            CartaMazoJugador.objects.filter(mazojugador=jugadorbatalla, carta=carta).first().delete()


    def jugar_carta(self,carta):
        manojugador = CartaManoJugador.objects.filter(carta=carta).first()
        carta_activa = CartaActivaJugador.objects.filter(batalla=manojugador.mano.batalla,turno=manojugador.mano.turno,jugador=manojugador.mano.jugador).first()
        reservajugador = ReservaJugador.objects.filter(batalla=manojugador.mano.batalla,turno=manojugador.mano.turno,jugador=manojugador.mano.jugador).first()
        if carta_activa:
            CartaReservaJugador.objects.create(carta=carta_activa, reserva=reservajugador)
            CartaActivaJugador.filter(batalla=manojugador.batalla,jugador=manojugador.jugador,turno=manojugador.turno).update(carta=carta)
        else:
            CartaActivaJugador.create(batalla=manojugador.batalla,turno=manojugador.turno,jugador=manojugador.jugador,carta=carta)
        CartaManoJugador.objects.filter(carta=carta).first().delete()


class CartaActivaJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo,on_delete=models.CASCADE, blank=True, null=True)

    def definir_carta_activa(self,carta):
        self.carta = carta
        self.save()


    def atacar(self,objetivo,ataque):
        objetivo.salud =- ataque.poder
        if objetivo.salud <= 0:
            objetivo.salud = 0
            carta_debilitada(objetivo)
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
        CartaActivaJugador.objets.filter(jugador=descarte.jugador).update(carta=None)


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
        self.accion = accion




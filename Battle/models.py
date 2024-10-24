import random
from Core.models import JugadorEntrenador, CartaMazo, Mazo

from django.db import models


class Batalla(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null= False)

    def save(self, *args, **kwargs):
        super(Batalla, self).save(*args, **kwargs)
        if not self.nombre:
            self.nombre = '{}_{}'.format(self.id, self.fecha)
            super(Batalla, self).save(*args, **kwargs)

    def registrar_batalla(self):
        self.objects.create()
        self.save()
        return self

    def __str__(self):
        return self.nombre

    def iniciar_batalla(self, jugador_1, jugador_2, mazo_1, mazo_2):
        batalla1=self.registrar_batalla()
        jugadorbatalla_1 = JugadorBatalla.registrar_jugadorbatalla(batalla1, jugador_1, mazo_1)
        jugadorbatalla_2 = JugadorBatalla.registrar_jugadorbatalla(batalla1,jugador_2,mazo_2)
        return jugadorbatalla_1, jugadorbatalla_2

    def batallar(self,jugador_1,jugador_2, mazo_1,mazo_2):
        jugadorbatalla_1,jugadorbatalla_2 = self.iniciar_batalla(jugador_1,jugador_2,mazo_1,mazo_2)
        id_turno = Turno.registrar_turno(jugadorbatalla_1.batalla)
        jugadoresbatalla = [jugadorbatalla_1,jugadorbatalla_2]
        for jugadorbatalla in jugadoresbatalla:
            TurnoJugador.registrar_turnojugador(id_turno,jugadorbatalla)
            CartaMazoJugador.llenar_mazo(jugadorbatalla, jugadorbatalla.mazo)

        while victoria == TRUE:

            Turno.empezar_turno(id_turno)

            Turno.actualizar_turno(jugadorbatalla_1.batalla)

        victoria()
        #CartaMazoJugador.robar_cartas(self,jugadorbatalla_1,mano,3)
        #CartaMazoJugador.robar_cartas(self,jugadorbatalla_2,mano,3)
        #Se debería crear función para hacer seguimiento del turno y no meter el turno en cada función.

class Turno(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.PositiveIntegerField(default=1)

    def registrar_turno(self,batalla):
        self.objects.create(batalla=batalla)
        self.save()
        return self
    def actualizar_turno(self,batalla):
        turno_anterior = self.objects.filter(batalla=batalla).first()
        este_turno= self.objects.create(batalla=batalla,turno=turno_anterior.turno)
        este_turno.turno += 1
        self.save()
    class Meta:
        unique_together = ('batalla', 'turno',)

    def empezar_turno(self,id_turno,jugadoresbatalla):
        for jugadorbatalla in jugadoresbatalla:
            TurnoJugador.empezar_turnojugador(jugadorbatalla)


class JugadorBatalla(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorEntrenador, on_delete=models.CASCADE)
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('batalla', 'jugador','mazo'),)

    def registrar_jugadorbatalla(self,batalla,jugador,mazo):
        self.objects.create(batalla=batalla, jugador=jugador, mazo=mazo)
        self.save()
        return self


class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugadorbatalla = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    energia = models.PositiveIntegerField(default=0) #pasar a jugadorbatalla

    class Meta:
        unique_together = ('turno', 'jugadorbatalla')

    def actualizar_turnojugador(self,id_turno,jugadorbatalla):
        self.turno = id_turno
        self.jugadorbatalla = jugadorbatalla
        self.save()

    def dar_energia(self,num_energia):
        self.energia += num_energia
        self.save()

    def registrar_turnojugador(self,id_turno,jugadorbatalla):
        turnojugador = self.objects.create(turno=id_turno, jugadorbatalla=jugadorbatalla)
        self.registrar_todo_por_turnojugador(turnojugador)
        self.save()

    def registrar_todo_por_turnojugador(self,turnojugador):
        CartaActivaJugador.registrar_cartaactivajugador(turnojugador)
        MazoJugador.registrar_mazojugador(turnojugador)
        ManoJugador.registrar_manojugador(turnojugador)
        DescartesJugador.registrar_descartesjugador(turnojugador)
        ReservaJugador.registrar_reservajugador(turnojugador)

    def empezar_turnojugador(self,jugadorbatalla):
        dar_energia(1)
        mazojugador = MazoJugador.objects.filter(jugador=jugadorbatalla).first()
        CartaMazoJugador.robar_cartas(mazojugador,1)

class MazoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_mazojugador(self,turnojugador):
        mazojugador = self.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador, jugador=turnojugador.jugadorbatalla)
        CartaMazoJugador.llenar_mazo(mazojugador,turnojugador.jugadorbatalla.mazo)
        self.save()

    def actualizar_mazojugador(self,turnojugador):
        mazojugador_anterior = self.objects.filter(jugador=turnojugador.jugadorbatalla).first()
        mazojugador_anterior.turno = turnojugador
        self.save()

class CartaMazoJugador(models.Model):
    mazojugador = models.ForeignKey(MazoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def llenar_mazo(self,mazojugador, mazo):
        cartas_en_mazo = CartaMazo.objects.filter(mazo=mazo)
        for carta in cartas_en_mazo:
            self.objects.create(mazojugador=mazojugador, carta=carta.carta)

    def robar_cartas(self, mazojugador, num_cartas): #REHACER
        cartas_disponibles = self.objects.filter(mazojugador=mazojugador)
        cartas_a_robar = random.sample(list(cartas_disponibles), min(num_cartas, len(cartas_disponibles)))
        turnojugador = MazoJugador.objects.filter(turno=mazojugador.turno).first()
        mano = ManoJugador.objects.filter(turno=turnojugador).first()

        for carta in cartas_a_robar:
            CartaManoJugador.objects.create(mano=mano, carta=carta)
            CartaMazoJugador.objects.filter(mazojugador=mazojugador, carta=carta).first().delete()


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_manojugador(self,turnojugador):
        self.create(batalla=turnojugador.batalla, turno=turnojugador, jugador=turnojugador.jugadorbatalla)
        self.save()

    def actualizar_manojugador(self,turnojugador):
        manojugador_anterior = self.objects.filter(jugador=turnojugador.jugadorbatalla).first()
        manojugador_anterior.turno = turnojugador
        self.save()


class CartaManoJugador(models.Model):
    mano = models.ForeignKey(ManoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def jugar_carta(self,carta):  #REVISAR
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

    def registrar_cartaactivajugador(self,turnojugador):
        self.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador,jugador=turnojugador.jugadorbatalla)
        self.save()

    def actualizar_cartaactivajugador(self,turnojugador):
        cartaactivajugador_anterior = self.objects.filter(jugador=turnojugador.jugadorbatalla).first()
        cartaactivajugador_anterior.turno = turnojugador
        self.save()

    def cambiar_carta_activa(self,carta):
        cartaactivajugador_anterior = self.objects.filter(jugador=carta.mano.jugadorbatalla).first()#REVISAR
        CartaReservaJugador.enviar_a_reserva(cartaactivajugador_anterior)
        cartaactivajugador_anterior.carta = carta.carta
        self.save()

    def atacar(self,objetivo,ataque):  #REHACER
        objetivo.salud =- ataque.poder
        if objetivo.salud <= 0:
            objetivo.salud = 0
            carta_debilitada(objetivo)
            ganar_punto(1)
        pass


class DescartesJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_descartesjugador(self,turnojugador):
        self.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador, jugadorbatalla=turnojugador.jugadorbatalla)
        self.save()

    def actualizar_descartesjugador(self,turnojugador):
        descartesjugador_anterior = self.objects.filter(jugador=turnojugador.jugadorbatalla).first()
        descartesjugador_anterior.turno = turnojugador
        self.save()

class CartaDescartesJugador(models.Model):
    descarte = models.ForeignKey(DescartesJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def carta_a_descartes(self, carta, descarte):
        self.objects.create(descarte=descarte,carta=carta)
        self.save()


class ReservaJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_reservajugador(self,turnojugador):
        self.create(batalla=turnojugador.jugadorbatalla.batalla,turno=turnojugador,jugadorbatalla=turnojugador.jugadorbatalla)
        self.save()

    def actualizar_reserva(self,turnojugador):
        reservajugador_anterior = self.objects.filter(jugador=turnojugador.jugadorbatalla).first()
        reservajugador_anterior.turno = turnojugador
        self.save()

class CartaReservaJugador(models.Model):
    reserva = models.ForeignKey(ReservaJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def rejugar_carta(self, carta_a_jugar,carta_a_reserva): #intercambiar carta_reserva y carta_activa
        self.objects.create(reserva=carta_a_jugar.reserva,carta=carta_a_reserva.carta)
        CartaActivaJugador.cambiar_carta_activa(carta_a_jugar)
        CartaReservaJugador.objects.filter(reserva=carta_a_jugar.reserva,carta=carta_a_jugar.carta).first().delete()
        self.save()

    def enviar_a_reserva(self,cartaactiva):
        turnojugador = CartaActivaJugador.objects.filter(turno=cartaactiva.turno).first()
        reserva = ReservaJugador.objects.filter(turno=turnojugador.turno).first()
        self.objects.create(reserva=reserva,carta=cartaactiva.carta)
        self.save()

class AccionTurnoJugador(models.Model):
    ACCION = [
        ('1', 'Ataque'),
        ('2', 'Pasar turno'),
        ('3', 'Recarga energía'),
        ('4', 'Jugar carta'),
    ]
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    accion = models.CharField(max_length=50, choices=ACCION, null=True, blank=True)

    def registrar_accion(self, turnojugador, accion, objetivo=None):
        self.objects.create(batalla=turnojugador.jugadorbatalla.batalla,turno=turnojugador,jugador=turnojugador.jugadorbatalla,accion=accion)
        self.save()
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

    def __str__(self):
        return self.nombre

    def iniciar_batalla(self, jugador_1, jugador_2, mazo_1, mazo_2):
        Batalla.registrar_batalla()
        JugadorBatalla.registrar_jugadorbatalla(batalla1, jugador_1, mazo_1)
        JugadorBatalla.registrar_jugadorbatalla(batalla1,jugador_2,mazo_2)
        jugadorbatalla_1 = JugadorBatalla.objects.filter(batalla=batalla1,jugador=jugador_1, mazo=mazo_1).first()
        jugadorbatalla_2 =JugadorBatalla.objects.filter(batalla=batalla1, jugador=jugador_2, mazo=mazo_2).first()
        return jugadorbatalla_1, jugadorbatalla_2

    def batallar(self,jugador_1,jugador_2, mazo_1,mazo_2):
        jugadorbatalla_1,jugadorbatalla_2 = self.iniciar_batalla(jugador_1,jugador_2,mazo_1,mazo_2)


        id_turno=Turno.registrar_turno(jugadorbatalla_1.batalla)

        TurnoJugador.registrar_turnojugador(self,id_turno,jugadorbatalla_1)
        TurnoJugador.registrar_todo_por_turnojugador(self,id_turno,jugadorbatalla_1)
        CartaMazoJugador.llenar_mazo(self, batalla1, jugadorbatalla_1, mazo_1)

        TurnoJugador.registrar_turnojugador(self, 1, jugadorbatalla_2)
        TurnoJugador.registrar_todo_por_turnojugador(self,1,jugadorbatalla_2)
        CartaMazoJugador.llenar_mazo(self, batalla1, jugadorbatalla_2, mazo_2)

        CartaMazoJugador.robar_cartas(self,jugadorbatalla_1,mano,3)
        CartaMazoJugador.robar_cartas(self,jugadorbatalla_2,mano,3)
        #Se debería crear función para hacer seguimiento del turno y no meter el turno en cada función.

class Turno(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.PositiveIntegerField(default=1)

    def registrar_turno(self,batalla):
        self.objects.create(batalla=batalla)
        self.save()
        return self
    def actualizar_turno(self,batalla):
        self.batalla = batalla
        self.turno += 1
        self.save()
    class Meta:
        unique_together = ('batalla', 'turno',)


class JugadorBatalla(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorEntrenador, on_delete=models.CASCADE)
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('batalla', 'jugador','mazo'),)

    def registrar_jugadorbatalla(self,batalla,jugador,mazo):
        jugador_batalla_1 = JugadorBatalla.objects.create(batalla=batalla, jugador=jugador, mazo=mazo)
        jugador_batalla_1.save()


class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugadorbatalla = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    energia = models.PositiveIntegerField(default=0) #pasar a jugadorbatalla

    class Meta:
        unique_together = ('turno', 'jugadorbatalla')

    def actualizar_turnojugador(self,id_turno,jugadorbatalla):
        self.turno = id_turno
        self.jugadorbatalla = jugadorbatalla
        self.energia += 1
        self.save()

    def registrar_turnojugador(self,id_turno,jugadorbatalla):
        FKturno_actual = Turno.objects.filter(turno=turno, batalla=jugadorbatalla.batalla).first()
        if turno > 1:
            FKturno_anterior = Turno.objects.filter(turno=turno-1,batalla=jugadorbatalla.batalla).first()
            energia_turno_anterior =TurnoJugador.objects.filter(turno=FKturno_anterior).energia
            energia_nueva = energia_turno_anterior + 1
            self.create(turno=FKturno_actual, jugadorbatalla=jugadorbatalla, energia=energia_nueva)
        else:

            self.create(turno=FKturno_actual, jugadorbatalla=jugadorbatalla, energia = 1)
        self.registrar_todo_por_turnojugador(turno,jugadorbatalla)
        self.save()

    def registrar_todo_por_turnojugador(self,turno, jugadorbatalla):
        batalla = JugadorBatalla.objects.filter(batalla=jugadorbatalla.batalla).first()
        if turno > 1:
            carta_activa = CartaActivaJugador.objects.filter(batalla=batalla,jugador=jugadorbatalla).last()
            if not carta_activa:
                CartaActivaJugador.registrar_cartaactivajugador(batalla, turno, jugadorbatalla)
            else:
                CartaActivaJugador.registrar_cartaactivajugador(batalla, turno, jugadorbatalla,carta_activa)
        else:
            CartaActivaJugador.registrar_cartaactivajugador(batalla, turno, jugadorbatalla)  # Si es 1r turno no hay registros
        MazoJugador.registrar_mazojugador(batalla,turno,jugadorbatalla)
        ManoJugador.registrar_manojugador(batalla,turno,jugadorbatalla)
        DescartesJugador.registrar_descartesjugador(batalla,turno,jugadorbatalla)
        ReservaJugador.registrar_reservajugador(batalla,turno,jugadorbatalla)
        if turno > 1:
            CartaMazoJugador.registrar_cartamazojugador(turno,mazojugador)
            CartaManoJugador.registrar_cartamanojugador(turno, manojugador)
            CartaDescartesJugador.registrar_cartadescartesjugador(turno, )
            CartaReservaJugador.registrar_cartareservajugador()


class MazoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_mazojugador(self,batalla,turno,jugadorbatalla):
        self.objects.create(batalla=batalla, turno=turno, jugador=jugadorbatalla)
        self.save()


class CartaMazoJugador(models.Model):
    mazojugador = models.ForeignKey(MazoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def registrar_cartamazojugador(self,turno,mazojugador):
        fk_turno_anterior= Turno.objects.filter(turno=turno-1, batalla=mazojugador.batalla).first()
        fk_mazojugador_anterior = MazoJugador.objects.filter(jugador=mazojugador.jugador,batalla=mazojugador.batalla,turno=fk_turno_anterior)
        cartas = self.objects.all(mazojugador=fk_mazojugador_anterior)
        for carta in cartas:
            self.objects.create(mazojugador=mazojugador,carta=carta.carta)
            self.save()

    def llenar_mazo(self, batalla, jugadorbatalla, mazo):
        FKturno1 = Turno.objects.filter(turno=1, batalla=jugadorbatalla.batalla).first()
        mazojugador = MazoJugador.objects.filter(batalla=batalla,jugador=jugadorbatalla,turno=FKturno1).first()
        cartas_en_mazo = CartaMazo.objects.filter(mazo=mazo)
        for carta in cartas_en_mazo:
            CartaMazoJugador.objects.create(mazojugador=mazojugador, carta=carta)

    def robar_cartas(self,jugadorbatalla,mano, num_cartas):
        cartas_disponibles = CartaMazoJugador.objects.filter(mazojugador=jugadorbatalla)
        cartas_a_robar = random.sample(list(cartas_disponibles), min(num_cartas, len(cartas_disponibles)))

        for carta in cartas_a_robar:
            CartaManoJugador.objects.create(mano=mano, carta=carta)
            CartaMazoJugador.objects.filter(mazojugador=jugadorbatalla, carta=carta).first().delete()


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_manojugador(self,batalla,turno,jugador):
        self.create(batalla=batalla, turno=turno, jugador=jugador)
        self.save()



class CartaManoJugador(models.Model):
    mano = models.ForeignKey(ManoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def registrar_cartamanojugador(self,turno,manojugador):
        for carta in cartas_mano_turno_anterior:
            CartaManoJugador.create(mano=manojugador,carta=carta.carta)
            CartaManoJugador.save()

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

    def registrar_carta_activa(self,batalla,turno,jugadorbatalla):
        FKturnoanterior = Turno.objects.filter(batalla=batalla,turno=turno-1) #Esta sobra creo
        carta_turno_anterior = CartaActivaJugador.objects.filter(batalla=batalla,jugador=jugadorbatalla).last()
        self.objects.create(batalla=batalla, turno=turno,jugador=jugadorbatalla,carta=carta_turno_anterior.carta)

    def cambiar_carta_activa(self,carta):
        self.carta = carta
        self.save()


    def atacar(self,objetivo,ataque):
        objetivo.salud =- ataque.poder
        if objetivo.salud <= 0:
            objetivo.salud = 0
            carta_debilitada(objetivo)
            ganar_punto(1)
        pass


class DescartesJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_descartesjugador(self,batalla,turno,jugadorbatalla):
        self.objects.create(batalla=batalla, turno=turno, jugadorbatalla=jugadorbatalla)
        self.save()

class CartaDescartesJugador(models.Model):
    descarte = models.ForeignKey(DescartesJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def registrar_cartadescartesjugador(self,turno,descartesjugador):
        for carta in cartas_descartes_turno_anterior:
            self.objects.create(descarte=descartesjugador,carta=carta.carta)

    def carta_debilitada(self, carta, descarte):
        CartaDescartesJugador.objects.create(descarte=descarte,carta=carta)
        CartaActivaJugador.objets.filter(jugador=descarte.jugador).update(carta=None)


class ReservaJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_reservajugador(self,batalla,turno,jugadorbatalla):
        self.create(batalla=batalla,turno=turno,jugadorbatalla=jugadorbatalla)
        self.save()

class CartaReservaJugador(models.Model):
    reserva = models.ForeignKey(ReservaJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def registrar_cartareservajugador(self,turno,reservajugador):
        for carta in cartas_reserva_turno_anterior:
            self.objects.create(reserva=reservajugador,carta=carta.carta)
            self.save()

    def rejugar_carta(self, carta_a_jugar,carta_a_reserva): #intercambiar carta_reserva y carta_activa
        CartaReservaJugador.objects.create(reserva=carta_a_jugar.reserva,carta=carta_a_reserva.carta)
        CartaReservaJugador.objects.filter(reserva=carta_a_jugar.reserva,carta=carta_a_jugar.carta).first().delete()
        CartaActivaJugador.cambiar_carta_activa(self, carta_a_jugar.carta)
        self.save()
        CartaActivaJugador.save()


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

    def registrar_accion(self, batalla, turno,jugadorbatalla, accion, objetivo=None):
        self.objects.create(batalla=batalla,turno=fkturno,jugador=jugadorbatalla,accion=accion)
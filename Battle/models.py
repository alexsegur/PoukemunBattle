import random
from Core.models import JugadorEntrenador, CartaMazo, Mazo
from django.db.models import Q, F

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


class Turno(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.PositiveIntegerField(default=0)

    def registrar_turno(self,batalla,turno):
        self.create(batalla=batalla,turno=turno)
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
        jugador_batalla_2 = JugadorBatalla.objects.create(batalla=batalla, jugador=jugador, mazo=mazo)
        jugador_batalla_1.save()
        jugador_batalla_2.save()


    def iniciar_batalla(self, jugador_1, jugador_2, mazo_1, mazo_2):
        Batalla.registrar_batalla()
        batalla1 = Batalla.objects.last()

        self.registrar_jugadorbatalla(batalla1, jugador_1, mazo_1)
        self.registrar_jugadorbatalla(batalla1,jugador_2,mazo_2)
        jugadorbatalla_1 = JugadorBatalla.objects.filter(batalla=batalla1,jugador=jugador_1, mazo=mazo_1).last()
        jugadorbatalla_2 = JugadorBatalla.objects.filter(batalla=batalla1, jugador=jugador_1, mazo=mazo_1).last()

        Turno.registrar_turno(self,batalla1,1)
        TurnoJugador.registrar_turnojugador(self,1,jugadorbatalla_1, 0)
        TurnoJugador.registrar_todo_por_turnojugador(self,1,jugadorbatalla_1)
        llenar_mazo(self, batalla1, jugadorbatalla_1, mazo_1)
        TurnoJugador.registrar_turnojugador(self, 1, jugadorbatalla_2, 0)
        TurnoJugador.registrar_todo_por_turnojugador(self,1,jugadorbatalla_2)
        llenar_mazo(self, batalla1, jugadorbatalla_2, mazo_2)

        robar_cartas(3,jugador_batalla_1,)
        robar_cartas(3,jugador_batalla_2,)


class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugadorbatalla = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    energia = models.PositiveIntegerField(default=0) #pasar a jugadorbatalla

    class Meta:
        unique_together = ('turno', 'jugadorbatalla')

    def registrar_turnojugador(self,turno,jugadorbatalla):
        FKturno_actual = Turno.objects.filter(turno=turno, batalla=jugadorbatalla.batalla).first()
        if turno > 1:
            FKturno_anterior = Turno.objects.filter(turno=F(turno-1),batalla=jugadorbatalla.batalla).first()
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
                registrar_cartaactivajugador(batalla, turno, jugadorbatalla)
            else:
                registrar_cartaactivajugador(batalla, turno, jugadorbatalla,carta_activa)
        else:
            registrar_cartaactivajugador(batalla, turno, jugadorbatalla)  # Si es 1r turno no hay registros
        registrar_mazojugador(batalla,turno,jugadorbatalla)
        registrar_manojugador(batalla,turno,jugadorbatalla)
        registrar_descartesjugador(batalla,turno,jugadorbatalla)
        registrar_reservajugador(batalla,turno,jugadorbatalla)
        if turno > 1:
            registrar_cartamazojugador(self,turno,mazojugador)
            registrar_cartamanojugador()
            registrar_cartadescartesjugador()
            registrar_cartareservajugador()


class MazoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def definir_mazo(self,batalla,turno,jugador):
        self.objects.create(batalla=batalla, turno=turno, jugador=jugador)
        self.save()


class CartaMazoJugador(models.Model):
    mazojugador = models.ForeignKey(MazoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def registrar_cartamazojugador(self,turno,mazojugador):
        FKturno_anterior= Turno.objects.filter(turno=F(turno-1), batalla=mazojugador.batalla).first()
        FKmazojugador_anterior = MazoJugador.objects.filter(jugador=mazojugador.jugador,batalla=mazojugador.batalla,turno=FKturno_anterior)
        cartas = self.objects.all(mazojugador=FKmazojugador_anterior)
        for carta in cartas:
            self.objects.create(mazojugador=mazojugador,carta=carta.carta)
            self.save()

    def llenar_mazo(self, batalla, jugadorbatalla, mazo):
        FKturno1 = Turno.objects.filter(turno=1, batalla=jugadorbatalla.batalla).first()
        mazojugador = MazoJugador.objects.filter(batalla=batalla,jugador=jugadorbatalla,turno=FKturno1).first()
        cartas_en_mazo = CartaMazo.objects.filter(mazo=mazo)
        for carta in cartas_en_mazo:
            CartaMazoJugador.objects.create(mazojugador=mazojugador, carta=carta)

    def robar_cartas(self,jugadorbatalla, mano, num_cartas):

        cartas_disponibles = CartaMazoJugador.objects.filter(mazojugador=jugadorbatalla)
        cartas_a_robar = random.sample(list(cartas_disponibles), min(num_cartas, len(cartas_disponibles)))

        for carta in cartas_a_robar:
            CartaManoJugador.objects.create(mano=mano, carta=carta)
            CartaMazoJugador.objects.filter(mazojugador=jugadorbatalla, carta=carta).first().delete()


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def definir_mano(self,batalla,turno,jugador):
        self.batalla = batalla
        self.turno = turno
        self.jugador = jugador



class CartaManoJugador(models.Model):
    mano = models.ForeignKey(ManoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

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

    def registrar_carta_activa(self,batalla,turno,jugador):
        FKturnoanterior = Truno.objects.filter(batalla=batalla,turno=F(turno-1))
        carta_turno_anterior = CartaActivaJugador.objects.filter(batalla=batalla,jugador=jugador).last()
        self.objects.create(batalla=batalla, turno=turno,jugador=jugador,carta=carta_turno_anterior.carta)
    def definir_carta_activa(self,carta):
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




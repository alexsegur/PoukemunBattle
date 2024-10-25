import random
from Core.models import JugadorEntrenador, CartaMazo, Mazo, CartaPokemon,CartaPokemonAtaque
from django.db import models


class Batalla(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null= False)

    def save(self, *args, **kwargs):
        super(Batalla, self).save(*args, **kwargs)
        if not self.nombre:
            self.nombre = '{}_{}'.format(self.id, self.fecha)
            super(Batalla, self).save(*args, **kwargs)

    @staticmethod
    def registrar_batalla():
        batalla = Batalla.objects.create()
        return batalla

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
            turnojugador = TurnoJugador.registrar_turnojugador(id_turno,jugadorbatalla)
            TurnoJugador.registrar_todo_por_turnojugador()
            CartaMazoJugador.llenar_mazo(jugadorbatalla, jugadorbatalla.mazo)
            mazojugador = MazoJugador.objects.filter(jugador=jugadorbatalla).first()
            CartaMazoJugador.robar_cartas(mazojugador,2)

        victoria = False
        while not victoria:
            Turno.empezar_turno(id_turno,victoria)
            if not victoria:
                Turno.actualizar_turno(jugadorbatalla_1.batalla)

        #CartaMazoJugador.robar_cartas(self,jugadorbatalla_1,mano,3)
        #CartaMazoJugador.robar_cartas(self,jugadorbatalla_2,mano,3)

class Turno(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.PositiveIntegerField(default=1)

    def registrar_turno(self,batalla):
        turno = Turno.objects.create(batalla=batalla)
        return turno
    def actualizar_turno(self,batalla):
        turno_anterior = Turno.objects.filter(batalla=batalla).order_by('id').last()
        Turno.objects.create(batalla=batalla,turno=turno_anterior.turno+1)

    class Meta:
        unique_together = ('batalla', 'turno',)

    def empezar_turno(self,jugadoresbatalla,victoria):
        for jugadorbatalla in jugadoresbatalla:
            TurnoJugador.empezar_turnojugador(jugadorbatalla)
            if victoria == True:
                return ganador



class JugadorBatalla(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorEntrenador, on_delete=models.CASCADE)
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE)
    puntos = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('batalla', 'jugador','mazo'),)

    def registrar_jugadorbatalla(self,batalla,jugador,mazo):
        jugadorbatalla = JugadorBatalla.objects.create(batalla=batalla, jugador=jugador, mazo=mazo)
        return jugadorbatalla

    def check_victoria(self,jugadorbatalla,victoria):
        jugadores = JugadorBatalla.objects.filter()
        if jugadorbatalla.puntos >= 2:
            victoria = True
            return victoria
        return victoria

    def ganar_punto(self,turnojugador):
        pass



class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugadorbatalla = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    energia = models.PositiveIntegerField(default=0)

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
        turnojugador = TurnoJugador.objects.create(turno=id_turno, jugadorbatalla=jugadorbatalla)
        return turnojugador

    @staticmethod
    def registrar_todo_por_turnojugador(turnojugador):
        CartaActivaJugador.registrar_cartaactivajugador(turnojugador)
        MazoJugador.registrar_mazojugador(turnojugador)
        ManoJugador.registrar_manojugador(turnojugador)
        DescartesJugador.registrar_descartesjugador(turnojugador)
        ReservaJugador.registrar_reservajugador(turnojugador)

    def empezar_turnojugador(self,jugadorbatalla,victoria):
        self.dar_energia(1)
        mazojugador = MazoJugador.objects.filter(jugador=jugadorbatalla).first()
        CartaMazoJugador.robar_cartas(mazojugador,1)
        final_turnojugador = False
        while not final_turnojugador:
            #Listener_de_accion #Debe retornar 'final_jugador = True' si la accion acaba el turno
            JugadorBatalla.check_victoria(jugadorbatalla,victoria)
        return victoria

class MazoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_mazojugador(self,turnojugador):
        mazojugador = MazoJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador, jugador=turnojugador.jugadorbatalla)
        CartaMazoJugador.llenar_mazo(mazojugador,turnojugador.jugadorbatalla.mazo)
        CartaMazoJugador.save()

    def actualizar_mazojugador(self,turnojugador):
        mazojugador_anterior = MazoJugador.objects.filter(jugador=turnojugador.jugadorbatalla).first()
        mazojugador_anterior.turno = turnojugador
        self.save()

class CartaMazoJugador(models.Model):
    mazojugador = models.ForeignKey(MazoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def llenar_mazo(self,mazojugador, mazo):
        cartas_en_mazo = CartaMazo.objects.filter(mazo=mazo)
        for carta in cartas_en_mazo:
            CartaMazoJugador.objects.create(mazojugador=mazojugador, carta=carta.carta)

    def robar_cartas(self, mazojugador, num_cartas):
        cartas_disponibles = CartaMazoJugador.objects.filter(mazojugador=mazojugador)
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
        ManoJugador.objects.create(batalla=turnojugador.batalla, turno=turnojugador, jugador=turnojugador.jugadorbatalla)

    def actualizar_manojugador(self,turnojugador):
        manojugador_anterior = ManoJugador.objects.filter(jugador=turnojugador.jugadorbatalla).first().update(turno=turnojugador)
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
        CartaActivaJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador,jugador=turnojugador.jugadorbatalla)

    def actualizar_cartaactivajugador(self,turnojugador):
        cartaactivajugador_anterior = CartaActivaJugador.objects.filter(jugador=turnojugador.jugadorbatalla).order_by("id").first()
        cartaactivajugador_anterior.turno = turnojugador
        cartaactivajugador_anterior.save()

    def cambiar_carta_activa(self,carta):
        cartaactivajugador_anterior = CartaActivaJugador.objects.filter(jugador=carta.mano.jugadorbatalla).order_by("id").first()
        cartaactivajugador_anterior.enviar_a_reserva()
        cartaactivajugador_anterior.carta = carta.carta
        carta.save()

    def enviar_a_reserva(self):
        reserva = ReservaJugador.objects.filter(turno=self.turno,jugador=self.jugador).order_by("id").first()
        try:
            ReservaJugador.objects.create(reserva=reserva,carta=self.carta)
        except:
            print(f"Has llegado al máximo de carta en reserva")

    def atacar(self,cartaactivaatacante, ataque, cartaactivaobjetivo):  #ACCION QUE ACABA TURNO
        salud_max = CartaPokemon.objects.filter(pokemon= cartaactivaobjetivo.carta.carta.pokemon).first().salud_max
        poder = CartaPokemonAtaque.objects.filter(id = ataque).first().damage
        contadores = poder/10
        carta_actualizada = ContadoresSaludCarta.anadir_contadores(objetivo.carta,contadores)
        if salud_max <= carta_actualizada.contadores * 10:
            JugadorBatalla.ganar_punto(cartaactivaatacante.jugador)
            CartaDescartesJugador.carta_a_descartes(cartaactivaobjetivo)
        final_turnojugador = True
        return final_turnojugador

class ContadoresSaludCarta(models.Model):
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)
    contadores = models.PositiveIntegerField(default=0)

    def anadir_contadores(self,cartamazo,contadores):
        carta_contadores = ContadoresSaludCarta.objects.filter(cartamazo=cartamazo).first()
        if carta_contadores.exists():
            contadores_totales = contadores + carta_contadores.contadores
            carta_actualizada = carta_contadores.objects.update(contadores=contadores_totales)
        else:
            carta_actualizada = ContadoresSaludCarta.objects.update(carta=cartamazo, contadores=contadores)

        return carta_actualizada





class DescartesJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_descartesjugador(self,turnojugador):
        DescartesJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador, jugadorbatalla=turnojugador.jugadorbatalla)

    def actualizar_descartesjugador(self,turnojugador):
        descartesjugador_anterior = DescartesJugador.objects.filter(jugador=turnojugador.jugadorbatalla).order_by("id").first()
        descartesjugador_anterior.turno = turnojugador
        descartesjugador_anterior.save()

class CartaDescartesJugador(models.Model):
    descarte = models.ForeignKey(DescartesJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    def carta_a_descartes(self, carta, descarte):
        CartaDescartesJugador.objects.create(descarte=descarte,carta=carta)


class ReservaJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    def registrar_reservajugador(self,turnojugador):
        ReservaJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla,turno=turnojugador,jugadorbatalla=turnojugador.jugadorbatalla)

    def actualizar_reserva(self,turnojugador):
        reservajugador_anterior = ReservaJugador.objects.filter(jugador=turnojugador.jugadorbatalla).first()
        reservajugador_anterior.turno = turnojugador
        self.save()

class CartaReservaJugador(models.Model):
    reserva = models.ForeignKey(ReservaJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('reserva', 'carta',)

    def rejugar_carta(self, carta_a_jugar,carta_a_reserva): #ACCION QUE NO ACABA TURNO
        carta_temporal = carta_a_jugar.carta
        carta_a_jugar.carta = carta_a_reserva.carta
        carta_a_reserva.carta = carta_temporal
        carta_a_jugar.save()
        carta_a_reseva.save()

    def clean(self):
        if self.jugador.cartareservajugador_set.count() >= 3:
            raise ValidationError("La reserva ya tiene el máximo de 3 cartas asignadas.")



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
        AccionTurnoJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla,turno=turnojugador,jugador=turnojugador.jugadorbatalla,accion=accion)
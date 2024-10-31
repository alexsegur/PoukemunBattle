import random
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from Core.models import JugadorEntrenador, CartaMazo, Mazo, CartaPokemon,CartaPokemonAtaque
from django.db import models


class Batalla(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=False)

    def save(self, *args, **kwargs):
        super(Batalla, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre or f"Batalla sin nombre"

    @staticmethod
    def registrar_batalla():
            batalla = Batalla.objects.create()
            print(f"Batalla creada con ID: {batalla.id}, campos {batalla.nombre},{batalla.fecha}")
            return batalla

    @staticmethod
    def iniciar_batalla(entrenador_1, entrenador_2, mazo_1, mazo_2):
        batalla = Batalla.registrar_batalla()

        jugadorbatalla_1 = JugadorBatalla.registrar_jugadorbatalla(batalla, entrenador_1, mazo_1)
        jugadorbatalla_2 = JugadorBatalla.registrar_jugadorbatalla(batalla, entrenador_2, mazo_2)
        jugadoresbatalla = [jugadorbatalla_1, jugadorbatalla_2]
        turno = Turno.registrar_turno(batalla)

        for jugadorbatalla in jugadoresbatalla:
            turnojugador = TurnoJugador.registrar_turnojugador(turno, jugadorbatalla)
            TurnoJugador.registrar_todo_por_turnojugador(turnojugador)
            mazojugador = MazoJugador.objects.get(jugador=jugadorbatalla, batalla=batalla, turno=turnojugador)
            CartaMazoJugador.robar_cartas(mazojugador, 2)

        return batalla, jugadoresbatalla

    def batallar(self,jugadoresbatalla):
        #jugadoresbatalla = self.iniciar_batalla(jugador_1,jugador_2, mazo_1,mazo_2)

        victoria = False
        while not victoria:
            Turno.realizar_turno(jugadoresbatalla)
            nuevo_turno = Turno.actualizar_turno()
            for jugadorbatalla in jugadoresbatalla:
                TurnoJugador.actualizar_turnojugador(nuevo_turno,jugadorbatalla)

# Señal post_save para asignar el nombre una vez que el objeto ya tiene un ID
@receiver(post_save, sender=Batalla)
def set_nombre_post_save(sender, instance, created, **kwargs):
    if created and not instance.nombre:
        # Genera el nombre usando id y la fecha
        instance.nombre = f"{instance.id}_{instance.fecha.strftime('%Y-%m-%d_%H-%M-%S')}"
        # Guarda solo el campo `nombre`
        instance.save(update_fields=['nombre'])


class Turno(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.PositiveIntegerField(default=1)

    @staticmethod
    def registrar_turno(batalla):
        return Turno.objects.create(batalla=batalla)

    @staticmethod
    def actualizar_turno(batalla):
        turno_anterior = Turno.objects.filter(batalla=batalla).lastest('turno').turno
        return Turno.objects.create(batalla=batalla, turno=turno_anterior + 1)

    @staticmethod
    def realizar_turno(jugadoresbatalla):
        for jugadorbatalla in jugadoresbatalla:
            TurnoJugador.preparar_turnojugador(jugadorbatalla)
            TurnoJugador.realizar_turnojugador(jugadorbatalla)


class JugadorBatalla(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorEntrenador, on_delete=models.CASCADE)
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE)
    puntos = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('batalla', 'jugador','mazo')

    @staticmethod
    def registrar_jugadorbatalla(batalla, jugador, mazo):
        return JugadorBatalla.objects.create(batalla=batalla, jugador=jugador, mazo=mazo)

    def ganar_punto(self, jugadorbatalla):
        jugadorbatalla.puntos += 1
        jugadorbatalla.save()
        jugadorbatalla.check_victoria()

    def check_victoria(self):
        jugadores = JugadorBatalla.objects.filter(batalla = self.batalla)
        for jugador in jugadores:
            if jugador.puntos >= 2:
                jugador.eres_ganador()

    def eres_ganador(self):
        print(f"{self.jugador.nombre} es el ganador",self)


class TurnoJugador(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    jugadorbatalla = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)
    energia = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('turno', 'jugadorbatalla')

    def actualizar_turnojugador(self,turno,jugadorbatalla): #REHACER
        TurnoJugador.objects.create(turno=turno, jugadorbatalla=jugadorbatalla)

    def dar_energia(self,num_energia):
        self.energia += num_energia
        self.save()

    @staticmethod
    def registrar_turnojugador(id_turno,jugadorbatalla):
        turnojugador = TurnoJugador.objects.create(turno=id_turno, jugadorbatalla=jugadorbatalla)
        return turnojugador


    @staticmethod
    def registrar_todo_por_turnojugador(turnojugador):
        CartaActivaJugador.registrar_cartaactivajugador(turnojugador)
        ManoJugador.registrar_manojugador(turnojugador)
        MazoJugador.registrar_mazojugador(turnojugador)
        DescartesJugador.registrar_descartesjugador(turnojugador)
        ReservaJugador.registrar_reservajugador(turnojugador)

    def preparar_turnojugador(self, jugadorbatalla):
        self.dar_energia(1)
        mazojugador = MazoJugador.objects.filter(jugador=jugadorbatalla).first()
        CartaMazoJugador.robar_cartas(mazojugador,1)

    def realizar_turnojugador(self, accion, jugadorbatalla):
            AccionTurnoJugador.registrar_accion() #Si la acción devuelve True se acaba el turno




class MazoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    @staticmethod
    def registrar_mazojugador(turnojugador):
        mazojugador = MazoJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador, jugador=turnojugador.jugadorbatalla)
        CartaMazoJugador.llenar_mazo(mazojugador,turnojugador.jugadorbatalla.mazo)

    def actualizar_mazojugador(self,turnojugador):
        mazojugador_anterior = MazoJugador.objects.filter(jugador=turnojugador.jugadorbatalla).first()
        mazojugador_anterior.turno = turnojugador
        self.save()

class CartaMazoJugador(models.Model):
    mazojugador = models.ForeignKey(MazoJugador, on_delete=models.CASCADE)
    carta = models.ForeignKey(CartaMazo, on_delete=models.CASCADE)
    @staticmethod
    def llenar_mazo(mazojugador, mazo):
        cartas_en_mazo = CartaMazo.objects.filter(mazo=mazo)
        for carta in cartas_en_mazo:
            CartaMazoJugador.objects.create(mazojugador=mazojugador, carta=carta)

    @staticmethod
    def robar_cartas(mazojugador, num_cartas):
        cartas_disponibles = CartaMazoJugador.objects.filter(mazojugador=mazojugador)
        cartas_a_robar = random.sample(list(cartas_disponibles), min(num_cartas, len(cartas_disponibles)))
        turnojugador = MazoJugador.objects.filter(turno=mazojugador.turno).first()
        mano = ManoJugador.objects.filter(turno=turnojugador.turno).first()

        for carta in cartas_a_robar:
            CartaManoJugador.objects.create(mano=mano, carta=carta.carta)
            CartaMazoJugador.objects.filter(mazojugador=mazojugador, carta=carta.carta).first().delete()


class ManoJugador(models.Model):
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE)

    @staticmethod
    def registrar_manojugador(turnojugador):
        ManoJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador, jugador=turnojugador.jugadorbatalla)

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

    @staticmethod
    def registrar_cartaactivajugador(turnojugador):
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
        carta_actualizada = ContadoresSaludCarta.anadir_contadores(cartaactivaobjetivo.carta,contadores)
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

    @staticmethod
    def registrar_descartesjugador(turnojugador):
        DescartesJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla, turno=turnojugador, jugador=turnojugador.jugadorbatalla)

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

    @staticmethod
    def registrar_reservajugador(turnojugador):
        ReservaJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla,turno=turnojugador,jugador=turnojugador.jugadorbatalla)

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
        carta_a_reserva.save()

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
    batalla = models.ForeignKey(Batalla, on_delete=models.CASCADE, null=True)
    turno = models.ForeignKey(TurnoJugador, on_delete=models.CASCADE,null=True)
    jugador = models.ForeignKey(JugadorBatalla, on_delete=models.CASCADE,null=True)
    accion = models.CharField(max_length=50, choices=ACCION, null=True, blank=True)

    def registrar_accion(self, turnojugador, accion, objetivo=None):
        AccionTurnoJugador.objects.create(batalla=turnojugador.jugadorbatalla.batalla,turno=turnojugador,jugador=turnojugador.jugadorbatalla,accion=accion)
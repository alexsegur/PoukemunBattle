from django.contrib import admin

from .models import Batalla, JugadorBatalla, CartaManoJugador, CartaDescartesJugador, CartaReservaJugador, TurnoJugador, \
    CartaActivaJugador,ManoJugador, DescartesJugador,ReservaJugador,Turno


class JugadorBatallaInline(admin.TabularInline):
    model = JugadorBatalla
    extra = 1


@admin.register(Batalla)
class BatallaJugadorAdmin(admin.ModelAdmin):
    list_display = ('id','nombre',)
    readonly_fields = ('nombre',)
    inlines = [JugadorBatallaInline]

class ManoJugadorTurnoInline(admin.TabularInline):
    model = CartaManoJugador

@admin.register(ManoJugador)
class ManoJugadorAdmin(admin.ModelAdmin):
    readonly_fields = ('batalla','turno','jugador')
    inlines = [ManoJugadorTurnoInline]


class DescartesJugadorTurnoInline(admin.TabularInline):
    model = CartaDescartesJugador

@admin.register(DescartesJugador)
class DescartesJugadorAdmin(admin.ModelAdmin):
    readonly_fields = ('batalla','turno','jugador')
    inlines = [DescartesJugadorTurnoInline]

class ReservaJugadorTurnoInline(admin.TabularInline):
    model = CartaReservaJugador

@admin.register(ReservaJugador)
class ReservaJugadorAdmin(admin.ModelAdmin):
    readonly_fields = ('batalla','turno','jugador')
    inlines = [ReservaJugadorTurnoInline]

class CartaActivaJugadorTurnoInline(admin.TabularInline):
    model = CartaActivaJugador

@admin.register(TurnoJugador)
class CartaActivaJugadorAdmin(admin.ModelAdmin):
    readonly_fields = ('batalla','turno','jugador','energia')
    inlines = [CartaActivaJugadorTurnoInline]




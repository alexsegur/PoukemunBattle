from django import forms
from .models import JugadorEntrenador
from Battle.models import AccionTurnoJugador

class PickEntrenadorForm(forms.Form):
    entrenador = forms.ModelChoiceField(queryset=JugadorEntrenador.objects.all(), label="Selecciona Entrenador")



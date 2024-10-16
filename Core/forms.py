from django import forms
from .models import JugadorEntrenador, Set


class BoosterPackForm(forms.Form):
    entrenador = forms.ModelChoiceField(queryset=JugadorEntrenador.objects.all(), label="Selecciona Entrenador")

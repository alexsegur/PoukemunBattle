from django import forms
from .models import JugadorEntrenador, Set


class PickEntrenadorForm(forms.Form):
    entrenador = forms.ModelChoiceField(queryset=JugadorEntrenador.objects.all(), label="Selecciona Entrenador")

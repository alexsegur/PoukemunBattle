from django import forms
from .models import JugadorEntrenador,Mazo


class GetPlayersForm(forms.Form):
    jugador_1 = forms.ModelChoiceField(queryset=JugadorEntrenador.objects.all(), label="Selecciona Jugador 1")
    mazo_1 = forms.ModelChoiceField(queryset=Mazo.objects.filter(entrenador=jugador_1).all(), label="Selecciona mazo del Jugador 1")

    jugador_2 = forms.ModelChoiceField(queryset=JugadorEntrenador.objects.all(), label="Selecciona Jugador 2")
    mazo_2 = forms.ModelChoiceField(queryset=Mazo.objects.filter(entrenador=jugador_2).all(), label="Selecciona mazo del Jugador 2")

    def clean(self):
        cleaned_data = super().clean()
        jugador_1 = cleaned_data.get("jugador_1")
        jugador_2 = cleaned_data.get("jugador_2")

        if jugador_1 and jugador_2 and jugador_1 == jugador_2:
            raise forms.ValidationError("Jugador 1 y Jugador 2 no pueden ser el mismo jugador.")

        return cleaned_data

class GetActionForm(forms.Form):
    pass
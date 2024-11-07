from django import forms
from .models import JugadorEntrenador, Mazo, AccionTurnoJugador


class GetPlayersForm(forms.Form):
    jugador_1 = forms.ModelChoiceField(queryset=JugadorEntrenador.objects.all(), label="Selecciona Jugador 1")
    jugador_2 = forms.ModelChoiceField(queryset=JugadorEntrenador.objects.all(), label="Selecciona Jugador 2")

    def clean(self):
        cleaned_data = super().clean()
        jugador_1 = cleaned_data.get("jugador_1")
        jugador_2 = cleaned_data.get("jugador_2")

        if jugador_1 and jugador_2 and jugador_1 == jugador_2:
            raise forms.ValidationError("Jugador 1 y Jugador 2 no pueden ser el mismo jugador.")

        return cleaned_data


class GetDecksForm(forms.Form):
    mazo_jugador_1 = forms.ModelChoiceField(queryset=Mazo.objects.none(), label="Selecciona mazo 1")
    mazo_jugador_2 = forms.ModelChoiceField(queryset=Mazo.objects.none(), label="Selecciona mazo 2")

    def __init__(self, *args, **kwargs):
        jugador_1 = kwargs.pop('jugador_1', None)
        jugador_2 = kwargs.pop('jugador_2', None)
        super().__init__(*args, **kwargs)

        if jugador_1:
            self.fields['mazo_jugador_1'].queryset = Mazo.objects.filter(entrenador=jugador_1)
        if jugador_2:
            self.fields['mazo_jugador_2'].queryset = Mazo.objects.filter(entrenador=jugador_2)

class PickActionForm(forms.Form):
    accion = forms.ChoiceField(choices=AccionTurnoJugador.ACCION, label="Elige una acción")

    tipo_ataque = forms.ChoiceField(
        label="Selecciona tipo de ataque",
        required=False,
        choices=[]
    )

    def __init__(self, *args, **kwargs):
        self.coleccion_id = kwargs.pop('coleccion_id', None)
        super().__init__(*args, **kwargs)

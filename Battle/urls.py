from django.urls import path

from .views import InicioDeBatallaView, SeleccionarJugadorView, SeleccionarMazoJugadorView

urlpatterns = [
    path('batalla/', InicioDeBatallaView.as_view(), name='mostrar_batalla'),
    path('selectJugadores/', SeleccionarJugadorView.as_view(), name='select_jugadores'),
    path('selectDecks/', SeleccionarMazoJugadorView.as_view(), name='select_mazos'),
]

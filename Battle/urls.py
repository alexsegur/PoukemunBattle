from django.urls import path

from .views import MostrarBatallaView, CrearBatallaView, SeleccionarMazoJugadorView

urlpatterns = [
    path('batalla/<int:batalla_id>/', MostrarBatallaView.as_view(), name='mostrar_batalla'),
    path('crearbatalla/', CrearBatallaView.as_view(), name='crear_batalla'),
    path('selectDecks/', SeleccionarMazoJugadorView.as_view(), name='select_mazos'),
]

from django.urls import path

from views import CrearBatallaView
from .views import MostrarBatallaView

urlpatterns = [
    path('batalla/<int:batalla_id>/', MostrarBatallaView.as_view(), name='mostrar_batalla'),
    path('crearbatalla/', CrearBatallaView.as_view(), name='crear_batalla'),
]
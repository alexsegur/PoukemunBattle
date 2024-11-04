from django.urls import path
from Core.views import IndexView, CollectionCardsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('show-collection/', CollectionCardsView.as_view(), name='view_collection'),
    path('open-booster/', IndexView.as_view(), name='open_booster')
]

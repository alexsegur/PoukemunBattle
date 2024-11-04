from django.urls import path
from Core.views import IndexView, CollectionCardsView,CompareCollectionToTotalView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('show-collection/', CollectionCardsView.as_view(), name='view_collection'),
    path('open-booster/', IndexView.as_view(), name='open_booster'),
    path('compare-collection-to-total/', CompareCollectionToTotalView.as_view(), name='compare_collection_to_total')
]

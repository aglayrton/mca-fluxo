from django.urls import path, include
from rest_framework import routers
from .views import FluxoViewSet, ConsumoDiarioView

router = routers.DefaultRouter()
router.register(r'fluxo', FluxoViewSet, basename='fluxo')

urlpatterns = [
    path('', include(router.urls)),
    path('consumo-diario/', ConsumoDiarioView.as_view() ,name='consumo_diario'),
]

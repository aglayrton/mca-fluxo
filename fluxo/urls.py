from django.urls import path, include
from rest_framework import routers
from .views import FluxoViewSet, ConsumoDiario

router = routers.DefaultRouter()
router.register(r'fluxo', FluxoViewSet, basename='fluxo')

urlpatterns = [
    path('', include(router.urls)),
    path('consumo-diario/', ConsumoDiario.as_view() ,name='consumo_diario'),
]

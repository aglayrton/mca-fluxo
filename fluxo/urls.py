from django.urls import path, include
from rest_framework import routers
from .views import FluxoViewSet, ConsumoDiarioView

router = routers.DefaultRouter()
router.register(r'fluxo', FluxoViewSet, basename='fluxo')
router.register(r'consumo-diario', ConsumoDiarioView, basename='consumo_diario')

urlpatterns = [
    path('', include(router.urls)),
]

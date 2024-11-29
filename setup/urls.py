from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from fluxo.views import FluxoViewSet

router = routers.DefaultRouter()

router.register('fluxo', FluxoViewSet, basename='Fluxo')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]

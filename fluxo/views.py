from fluxo.models import FluxoAgua
from fluxo.serializers import FluxoAguaSerializer
from rest_framework import viewsets

class FluxoViewSet(viewsets.ModelViewSet):
    queryset = FluxoAgua.objects.all()
    serializer_class = FluxoAguaSerializer
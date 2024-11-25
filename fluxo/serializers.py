from rest_framework import serializers
from fluxo.models import FluxoAgua

class FluxoAguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FluxoAgua
        fields = ['consumo_diario', 'data']
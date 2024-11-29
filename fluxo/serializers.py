from rest_framework import serializers
from .models import FluxoAgua, Consumo
from django.utils import timezone

class FluxoAguaSerializer(serializers.ModelSerializer):
    data_hora = serializers.SerializerMethodField()

    class Meta:
        model = FluxoAgua
        fields = ['data_hora', 'litros']

    def get_data_hora(self, obj):
        local_time = timezone.localtime(obj.data_hora)
        return local_time.strftime('%d/%m/%Y %H:%M:%S')


class ConsumoSerializer(serializers.ModelSerializer):
    hora_consumo = serializers.SerializerMethodField()
    data_consumo = serializers.SerializerMethodField()

    class Meta:
        model = Consumo
        fields = ['consumo', 'hora_consumo', 'data_consumo']
        read_only_fields = ['hora_consumo', 'data_consumo']

    def get_hora_consumo(self, obj):
        local_time = timezone.localtime(obj.data_hora)
        return local_time.strftime('%H:%M:%S')

    def get_data_consumo(self, obj):
        local_time = timezone.localtime(obj.data_hora)
        return local_time.strftime('%d/%m/%Y')

    def validate_consumo(self, value):
        if value < 0:
            raise serializers.ValidationError("O consumo não pode ser negativo.")
        return value

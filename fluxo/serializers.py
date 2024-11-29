from rest_framework import serializers
from .models import FluxoAgua, ConsumoDiario
from django.utils import timezone

class FluxoAguaSerializer(serializers.ModelSerializer):
    data_hora = serializers.SerializerMethodField()
    consumo_diario = serializers.CharField()

    class Meta:
        model = FluxoAgua
        fields = ['data_hora', 'consumo_diario']

    def get_data_hora(self, obj):
        local_time = timezone.localtime(obj.data_hora)
        return local_time.strftime('%d/%m/%Y %H:%M:%S')

    def create(self, validated_data):
        consumo_diario_str = validated_data.get('consumo_diario')
        consumo_diario = float(consumo_diario_str)
        fluxo = FluxoAgua.objects.create(consumo_diario=consumo_diario)
        return fluxo

    def validate_consumo_diario(self, value):
        try:
            consumo_diario = float(value)
            if consumo_diario <= 0:
                raise serializers.ValidationError("O valor de consumo_diario deve ser positivo.")
            return value
        except ValueError:
            raise serializers.ValidationError("O consumo_diario deve ser um número válido.")

# Adjusted Serializer to reference ConsumoDiario
class ConsumoDiarioSerializer(serializers.ModelSerializer):
    hora = serializers.SerializerMethodField()

    class Meta:
        model = ConsumoDiario  # Changed from Consumo to ConsumoDiario
        fields = ['data', 'hora', 'consumo_total']
        read_only_fields = ['hora']

    def get_hora(self, obj):
        return obj.hora.strftime('%H:%M:%S')

    def validate_consumo_total(self, value):
        if value < 0:
            raise serializers.ValidationError("O consumo_total não pode ser negativo.")
        return value

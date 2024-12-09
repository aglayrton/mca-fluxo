from decimal import Decimal
from django.utils import timezone
from rest_framework import serializers
from .models import FluxoAgua, ConsumoDiario

class FluxoAguaSerializer(serializers.ModelSerializer):
    data_hora = serializers.SerializerMethodField()
    litros = serializers.DecimalField(source='valor', max_digits=10, decimal_places=2, read_only=True)
    consumo_diario = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    class Meta:
        model = FluxoAgua
        fields = ['data_hora', 'litros', 'consumo_diario']

    def get_data_hora(self, obj):
        local_time = timezone.localtime(obj.data_hora)
        return local_time.strftime('%d/%m/%Y %H:%M:%S')

    def validate_consumo_diario(self, value):
        if value < 0:
            raise serializers.ValidationError("O consumo_diario deve ser um valor positivo.")
        return value

    def create(self, validated_data):
        leitura_atual = validated_data.get('consumo_diario', Decimal('0.00'))
        agora = timezone.localtime()
        hoje = agora.date()
        ultima_leitura = FluxoAgua.objects.filter(data_hora__date=hoje).order_by('-data_hora').first()

        if ultima_leitura:
            valor_anterior = ultima_leitura.valor
            if leitura_atual > valor_anterior:
                diferenca = leitura_atual - valor_anterior
            else:
                diferenca = leitura_atual
        else:
            diferenca = leitura_atual

        fluxo = FluxoAgua.objects.create(valor=leitura_atual)

        consumo_diario_obj, criado = ConsumoDiario.objects.get_or_create(
            data=hoje,
            defaults={
                'consumo_total': diferenca,
                'hora': timezone.localtime(fluxo.data_hora).time()
            }
        )

        if not criado:
            consumo_diario_obj.consumo_total += diferenca
            consumo_diario_obj.hora = timezone.localtime(fluxo.data_hora).time()
            consumo_diario_obj.save()

        return fluxo


class ConsumoDiarioSerializer(serializers.ModelSerializer):
    hora = serializers.SerializerMethodField()

    class Meta:
        model = ConsumoDiario
        fields = ['data', 'hora', 'consumo_total']
        read_only_fields = ['hora']

    def get_hora(self, obj):
        return obj.hora.strftime('%H:%M:%S') if obj.hora else "Sem dados"

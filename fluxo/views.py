from datetime import timedelta
from decimal import Decimal
from django.db.models import Sum
from django.utils.timezone import localtime
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet, mixins
from .models import FluxoAgua, ConsumoDiario
from .serializers import FluxoAguaSerializer, ConsumoDiarioSerializer

class FluxoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = FluxoAguaSerializer

    def get_queryset(self):
        today = localtime().date()
        return FluxoAgua.objects.filter(data_hora__date=today).order_by('-data_hora')


class ConsumoDiarioView(ViewSet):
    def list(self, request):
        now = localtime()
        hoje = now.date()
        ontem = hoje - timedelta(days=1)

        if not ConsumoDiario.objects.filter(data=ontem).exists():
            consumo_ontem = FluxoAgua.objects.filter(data_hora__date=ontem).aggregate(
                total=Sum('valor')
            )['total'] or Decimal('0.00')
            ultima_leitura_ontem = FluxoAgua.objects.filter(data_hora__date=ontem).order_by('-data_hora').first()
            hora_ultima_alteracao = ultima_leitura_ontem.data_hora.time() if ultima_leitura_ontem else None

            ConsumoDiario.objects.create(
                data=ontem,
                consumo_total=consumo_ontem,
                hora=hora_ultima_alteracao
            )

        consumo_diario_obj = ConsumoDiario.objects.filter(data=hoje).first()
        if consumo_diario_obj:
            consumo_total_valor = consumo_diario_obj.consumo_total
            ultima_hora = consumo_diario_obj.hora.strftime('%H:%M:%S') if consumo_diario_obj.hora else "Sem dados"
        else:
            consumo_total_valor = Decimal('0.00')
            ultima_hora = "Sem dados"

        return Response({
            "data": now.strftime('%d/%m/%Y'),
            "hora": ultima_hora,
            "consumo_diario": str(consumo_total_valor)
        })

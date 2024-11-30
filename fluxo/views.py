from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.utils.timezone import localtime
from datetime import date, timedelta
import logging
from .models import FluxoAgua, ConsumoDiario
from .serializers import FluxoAguaSerializer, ConsumoDiarioSerializer

logger = logging.getLogger(__name__)

class FluxoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FluxoAguaSerializer

    def get_queryset(self):
        today = localtime().date()
        return FluxoAgua.objects.filter(data_hora__date=today).order_by('-data_hora')

class ConsumoDiarioView(APIView):
    def get(self, request):
        now = localtime()
        hoje = now.date()
        ontem = hoje - timedelta(days=1)

        if not ConsumoDiario.objects.filter(data=ontem).exists():
            consumo_ontem = FluxoAgua.objects.filter(data_hora__date=ontem).aggregate(
                total=Sum('consumo_diario')
            )['total'] or 0
            ultima_hora_ontem = FluxoAgua.objects.filter(data_hora__date=ontem).order_by('-data_hora').first()
            hora_ultima_alteracao = ultima_hora_ontem.data_hora.time() if ultima_hora_ontem else None

            ConsumoDiario.objects.create(
                data=ontem,
                consumo_total=consumo_ontem,
                hora=hora_ultima_alteracao
            )

        consumo_total = FluxoAgua.objects.filter(data_hora__date=hoje).aggregate(
            total=Sum('consumo_diario')
        )['total'] or 0
        ultima_modificacao = FluxoAgua.objects.filter(data_hora__date=hoje).order_by('-data_hora').first()
        ultima_hora = ultima_modificacao.data_hora.strftime('%H:%M:%S') if ultima_modificacao else "Sem dados"

        return Response({
            "data": now.strftime('%d/%m/%Y'),
            "hora": ultima_hora,
            "consumo_diario": consumo_total
        })


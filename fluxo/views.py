from rest_framework import viewsets, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import date
import logging
from .models import FluxoAgua, Consumo
from .serializers import FluxoAguaSerializer, ConsumoSerializer

logger = logging.getLogger(__name__)

class FluxoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FluxoAguaSerializer

    def get_queryset(self):
        today = timezone.localtime().date()
        return FluxoAgua.objects.filter(data_hora__date=today).order_by('-data_hora')


class ConsumoDiario(APIView):
    def get(self, request):
        now = timezone.localtime()
        hoje = now.date()
        consumo_total = FluxoAgua.objects.filter(data_hora__date=hoje).aggregate(total=Sum('litros'))['total'] or 0

        return Response({
            "data": now.strftime('%d/%m/%Y'),
            "hora": now.strftime('%H:%M:%S'),
            "consumo_diario": consumo_total
        }, status=status.HTTP_200_OK)

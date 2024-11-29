from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FluxoAgua, Consumo
from .serializers import FluxoAguaSerializer, ConsumoSerializer
from django.db.models import Sum
from django.utils import timezone
from datetime import date
import logging

logger = logging.getLogger(__name__)

class FluxoViewSet(viewsets.ModelViewSet):
    queryset = FluxoAgua.objects.all()
    serializer_class = FluxoAguaSerializer

class ConsumoDiario(APIView):
    def get(self, request, format=None):
        hoje = timezone.localtime().date()

        try:
            fluxo = FluxoAgua.objects.get(data=hoje)

            return Response({'data': fluxo.data.strftime('%d/%m/%Y'), 'hora': fluxo.hora.strftime('%H:%M:%S'), 'consumo_diario_total': fluxo.consumo_diario}, status=status.HTTP_200_OK)

        except FluxoAgua.DoesNotExist:
            return Response({'message': 'Nenhum consumo registrado para o dia de hoje.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = ConsumoSerializer(data=request.data)
        if serializer.is_valid():
            consumo = serializer.save()
            agora = timezone.localtime(consumo.data_hora)
            hoje = agora.date()

            consumo_total = Consumo.objects.filter(data_hora__date=hoje).aggregate(total=Sum('consumo'))['total'] or 0

            FluxoAgua.objects.update_or_create(
                data=hoje,
                defaults={'consumo_diario': consumo_total, 'hora': agora.time()}
            )

            logger.info(f"Consumo registrado: {serializer.data}")

            return Response({'message': 'Consumo registrado com sucesso'}, status=status.HTTP_201_CREATED)
        
        logger.error(f"Erro ao registrar consumo: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


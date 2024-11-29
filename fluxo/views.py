from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FluxoAgua, Consumo
from .serializers import FluxoAguaSerializer, ConsumoSerializer
from django.db.models import Sum
from django.utils import timezone
from datetime import date

class FluxoViewSet(viewsets.ModelViewSet):
    queryset = FluxoAgua.objects.all()
    serializer_class = FluxoAguaSerializer

class ConsumoDiario(APIView):

    def get(self, request, format=None):

        hoje = timezone.localtime().date()

        consumo_total = Consumo.objects.filter(data_hora__date=hoje).aggregate(total=Sum('consumo'))['total'] or 0

 
        ultimo_consumo = Consumo.objects.filter(data_hora__date=hoje).order_by('-data_hora').first()

        if ultimo_consumo:

            serializer = ConsumoSerializer(ultimo_consumo)
            ultimo_consumo_hora = serializer.data['hora_consumo']
            ultimo_consumo_data = serializer.data['data_consumo']
        else:
            ultimo_consumo_hora = None
            ultimo_consumo_data = None

        return Response({'Data': ultimo_consumo_data, 'Hora': ultimo_consumo_hora, 'Consumo_Diario_Total': consumo_total}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
 
        serializer = ConsumoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Consumo registrado com sucesso'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

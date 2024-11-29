from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Consumo, FluxoAgua
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class ConsumoDiarioTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('consumo_diario')  # Nome definido no urls.py para o endpoint
        self.hoje = timezone.localtime().date()

    def test_get_sem_registros(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Nenhum consumo registrado para o dia de hoje.')

    def test_post_consumo_valido(self):

        data = {'consumo': 1.25}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Consumo registrado com sucesso')
        self.assertEqual(Consumo.objects.count(), 1)
        self.assertEqual(FluxoAgua.objects.count(), 1)

        fluxo = FluxoAgua.objects.get(data=self.hoje)
        self.assertEqual(fluxo.consumo_diario, 1.25)

    def test_post_consumo_negativo(self):

        data = {'consumo': -1.25}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('consumo', response.data)
        self.assertEqual(response.data['consumo'][0], 'O consumo não pode ser negativo.')
        self.assertEqual(Consumo.objects.count(), 0)
        self.assertEqual(FluxoAgua.objects.count(), 0)

    def test_get_com_registros(self):

        Consumo.objects.create(consumo=1.25, data_hora=timezone.localtime())
        Consumo.objects.create(consumo=2.50, data_hora=timezone.localtime())
        consumo_total = Consumo.objects.filter(data_hora__date=self.hoje).aggregate(total=Sum('consumo'))['total'] or 0
        FluxoAgua.objects.create(data=self.hoje, consumo_diario=consumo_total, hora=timezone.localtime().time())

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], self.hoje.strftime('%d/%m/%Y'))
        self.assertEqual(response.data['hora'], timezone.localtime().strftime('%H:%M:%S'))
        self.assertEqual(response.data['consumo_diario_total'], consumo_total)

    def test_post_cria_registro_para_novo_dia(self):

	    ontem = self.hoje - timedelta(days=1)

	    Consumo.objects.create(consumo=2.50, data_hora=timezone.now() - timedelta(days=1))
	    FluxoAgua.objects.create(data=ontem, consumo_diario=2.50, hora=(timezone.now() - timedelta(days=1)).time())

	    data = {'consumo': 1.50}
	    response = self.client.post(self.url, data, format='json')
	    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	    self.assertEqual(FluxoAgua.objects.count(), 2)

	    fluxo_hoje = FluxoAgua.objects.get(data=self.hoje)
	    self.assertEqual(float(fluxo_hoje.consumo_diario), 1.50)

	    fluxo_ontem = FluxoAgua.objects.get(data=ontem)
	    self.assertEqual(float(fluxo_ontem.consumo_diario), 2.50)



from django.db import models

class FluxoAgua(models.Model):
    consumo_diario = models.CharField(name='consumo_diario', max_length= 30)
    data = models.CharField(name='data', max_length=50)
    
    def __str__(self):
        return self.consumo_diario
from django.db import models

# Create your models here.
class FinancialData(models.Model):
    symbol = models.CharField(max_length=55)
    date = models.DateField() 
    open_price = models.FloatField()
    close_price= models.FloatField()
    volume = models.IntegerField()

    class Meta:
        unique_together = ['symbol', 'date']
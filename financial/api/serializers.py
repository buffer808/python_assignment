from rest_framework import routers, serializers, viewsets
from .models import FinancialData


class FinancialDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FinancialData
        fields = ['symbol', 'date', 'open_price', 'close_price', 'volume']
from django.urls import path
from api.views import FinancialDataView

urlpatterns = [
    path('financial_data/', FinancialDataView.getData)
]
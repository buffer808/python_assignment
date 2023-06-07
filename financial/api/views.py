from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
from .serializers import FinancialDataSerializer
from .models import FinancialData
from django.db.models import Q
import datetime

class FinancialDataView:
    
    @api_view(['GET'])
    def getData(request):
        output = {
            'pagination': {
                'count': 0,
                'page': 0,
                'limit': 0,
                'pages': 0,
            },
            'data':[],
            'info':{'error':''}
        }
        
        try:
            start_date = request.GET.get('start_date') or None
            end_date = request.GET.get('end_date') or None
            symbol = request.GET.get('symbol') or None
            limit = request.GET.get('limit') or '5'
            page = request.GET.get('page') or '1'
            data_obj = FinancialData.objects
            
            if symbol is not None:
                data_obj = data_obj.filter(symbol=symbol)
                
            if start_date and end_date:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                data_obj = data_obj.filter(date__range=(start_date,end_date))
            elif start_date and not end_date:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                data_obj = data_obj.filter(Q(date__gte=start_date))
            elif end_date and not start_date:
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                data_obj = data_obj.filter(Q(date__lte=end_date))
            else:
                data_obj = data_obj.all()
                
            paginator = Paginator(data_obj, int(limit))
            
            financial_data = FinancialDataSerializer(paginator.get_page(int(page)).object_list, many=True)
            
            output.update({
                'pagination': {
                    'count': paginator.count,
                    'page' : int(page),
                    'limit' : int(limit),
                    'pages' : paginator.num_pages,
                }
            })
            output.update({'data': financial_data.data})
            
        except Exception as e:
            error = str(e)
            output['info']['error'] = error
            
        
        
        return Response(output)
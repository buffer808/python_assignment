from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
from .serializers import FinancialDataSerializer
from .models import FinancialData
from django.db.models import Q
import numpy as np
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
    
    @api_view(['GET'])
    def getStatistics(request):
        def _get_avg(key, data):
            try:
                row_count = data.count()
                row_data = [getattr(i, key) for i in data]
                row_arr = np.array(row_data).reshape(row_count, 1)
                return np.mean(row_arr)
            except Exception as e:
                pass
            
        output = {
            'data':[],
            'info':{'error':''}
        }
        
        try:
            start_date = request.GET.get('start_date') or None
            end_date = request.GET.get('end_date') or None
            symbol = request.GET.get('symbol') or None
            
            if not start_date:
                raise Exception('`start_date` parameter is required.')
            
            if not end_date:
                raise Exception('`end_date` parameter is required.')
            
            if not symbol:
                raise Exception('`symbol` parameter is required.')
            
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            
            financial_data = FinancialData.objects.filter(symbol=symbol).filter(date__range=(start_date,end_date))
            
            if not financial_data.count():
                raise Exception('No records were found.')
            
            avg_open_prices = _get_avg('open_price', financial_data)
            avg_close_prices = _get_avg('close_price', financial_data)
            avg_volumes = _get_avg('volume', financial_data)
            
            output.update({'data': {
                "start_date" : start_date,
                "end_date" : end_date,
                "symbol" : symbol,
                "average_daily_open_price" : format(avg_open_prices, '.2f'),
                "average_daily_close_price" : format(avg_close_prices, '.2f'),
                "average_daily_volume" : format(avg_volumes, '.2f'),
            }})
            
        except Exception as e:
            error = str(e)
            output['info']['error'] = error
        
        return Response(output)
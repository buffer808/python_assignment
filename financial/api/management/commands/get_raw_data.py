from django.core.management.base import BaseCommand
from api.models import FinancialData
from alpha_vantage.timeseries import TimeSeries
import os, datetime, json

class Command(BaseCommand):
    help = "Retrieve the financial data of Two given stocks (IBM, Apple Inc.)for the most recently two weeks. Using a free API provider named AlphaVantage"
    output_data = []
    
    stocks = ['IBM','AAPL']
    
    def handle(self, *args, **options):
        
        # Set your AlphaVantage API key here
        API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')

        # Get the current date
        current_date = datetime.date.today()

        # Get the date 2 weeks ago
        weeks_delta = datetime.timedelta(weeks=2)
        two_weeks_ago = current_date - weeks_delta

        # Create a TimeSeries object with your API key
        ts = TimeSeries(key=API_KEY)
        
        for stock in self.stocks:
            stock_data, stock_meta_data = ts.get_daily_adjusted(symbol=stock, outputsize='compact')
            
            for date, data in stock_data.items():
                parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                if parsed_date >= two_weeks_ago:
                    self._storeData(stock, parsed_date, data)
                    self._updateOutputData(
                        stock, str(parsed_date), data['1. open'],  data['4. close'],  data['6. volume']
                    )
                    continue
        
        print(json.dumps(self.output_data))
                
    # Store the data to financial_data table
    def _storeData(self, symbol, date, data):
        try:
            financial_data = FinancialData()
            financial_data.symbol = symbol
            financial_data.date = date
            financial_data.open_price = float(data['1. open'])
            financial_data.close_price = float(data['4. close'])
            financial_data.volume = int(data['6. volume'])
            financial_data.save() 
        except Exception as e:
            if('duplicate key value violates unique constraint' not in str(e)):
                raise Exception(str(e))
            
    def _updateOutputData(self, symbol, date, open, close, volume):
        self.output_data.append({
            'symbol': symbol,
            'date': date,
            'open_price': float(open), 
            'close_price': float(close), 
            'volume': int(volume)
        })
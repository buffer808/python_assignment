from django.core.management.base import BaseCommand
from api.models import FinancialData
from alpha_vantage.timeseries import TimeSeries
import os, datetime, json

class Command(BaseCommand):
    help = "Retrieve the financial data of Two given stocks (IBM, Apple Inc.)for the most recently two weeks. Using a free API provider named AlphaVantage"
    
    def handle(self, *args, **options):
        
        # Set your AlphaVantage API key here
        API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')

        # Get the current date
        current_date = datetime.date.today()

        # Calculate the date 2 weeks ago
        weeks_delta = datetime.timedelta(weeks=2)
        two_weeks_ago = current_date - weeks_delta

        # Create a TimeSeries object with your API key
        ts = TimeSeries(key=API_KEY)

        # Retrieve the stock data for IBM
        ibm_data, ibm_meta_data = ts.get_daily_adjusted(symbol='IBM', outputsize='full')

        # Retrieve the stock data for Apple Inc.
        apple_data, apple_meta_data = ts.get_daily_adjusted(symbol='AAPL', outputsize='full')

        # Print the recent two weeks of data for IBM
        self.stdout.write("IBM Stock Data:")
        output_data = []
        
        for date, data in ibm_data.items():
            parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if parsed_date >= two_weeks_ago:
                self.storeData('IBM', parsed_date, data)
                output_data.append({
                    'symbol': 'IBM',
                    'date': str(parsed_date),
                    'open_price': float(data['1. open']), 
                    'close_price': float(data['4. close']), 
                    'volume': int(data['6. volume'])
                })
                continue
                        
                

        # Print the recent two weeks of data for Apple Inc.
        print("\nApple Inc. Stock Data:")
        for date, data in apple_data.items():
            parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if parsed_date >= two_weeks_ago:
                self.storeData('AAPL', parsed_date, data)
                output_data.append({
                    'symbol': 'IBM',
                    'date': str(parsed_date),
                    'open_price': float(data['1. open']), 
                    'close_price': float(data['4. close']), 
                    'volume': int(data['6. volume'])
                })
                continue
        
        print(json.dumps(output_data))
                
    # Store the data to financial_data table
    def storeData(self, symbol, date, data):
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
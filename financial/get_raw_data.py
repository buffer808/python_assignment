from alpha_vantage.timeseries import TimeSeries
import datetime

# Set your AlphaVantage API key here
API_KEY = "77ZETABJMGUU5A66"

# Get the current date
current_date = datetime.date.today()

# Calculate the date 2 weeks ago
weeks_delta = datetime.timedelta(weeks=2)
two_weeks_ago = current_date - weeks_delta

# Create a TimeSeries object with your API key
ts = TimeSeries(key=API_KEY)

# Retrieve the stock data for IBM
ibm_data, ibm_meta_data = ts.get_daily_adjusted(symbol='IBM', outputsize='compact')

# Retrieve the stock data for Apple Inc.
apple_data, apple_meta_data = ts.get_daily_adjusted(symbol='AAPL', outputsize='compact')

# Print the recent two weeks of data for IBM
print("IBM Stock Data:")
for date, data in ibm_data.items():
    parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    # if two_weeks_ago > 
    print(date, data)

# Print the recent two weeks of data for Apple Inc.
print("\nApple Inc. Stock Data:")
for date, data in apple_data.items():
    print(date, data)

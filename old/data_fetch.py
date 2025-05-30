import requests
API_KEY = '69LK6GFJKXIAFUI9'

def get_data(key):
    """Fetches the latest data from the API and returns it as a dictionary."""
    # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=INTC&interval=5min&apikey={key}'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=NYSE&outputsize=full&apikey={key}'
    response = requests.get(url)
    return response.json()

    # url = f'https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=true&market_data=true&community_data=true&developer_data=true&sparkline=true'
    # response = requests.get(url)
    # return response.json()

print(get_data(API_KEY))
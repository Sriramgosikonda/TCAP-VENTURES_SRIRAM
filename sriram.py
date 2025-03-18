import requests
import pandas as pd
import os

class DataIngestion:
    def __init__(self, symbol="BTCUSDT", interval="1m", limit=100):
        self.api_url = f"https://crypto-intraday.com/api/fetch/binance?symbol={symbol}&interval={interval}&limit={limit}"
        self.symbol = symbol
        self.data_folder = "data"
        os.makedirs(self.data_folder, exist_ok=True)
    
    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            data = response.json()
            
            # Convert API response to DataFrame
            df = pd.DataFrame(data)
            
            # Rename columns to standard format
            df.rename(columns={
                'OpenTime': 'timestamp',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume',
                'CloseTime': 'close_time'
            }, inplace=True)
            
            # Convert timestamps to human-readable format
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

            # Save the data
            df.to_csv(f"{self.data_folder}/{self.symbol}_data.csv", index=False)
            
            return df
        else:
            print("Error fetching data")
            return None

# Fetch and save data
ingestor = DataIngestion()
df = ingestor.fetch_data()
print(df.head())

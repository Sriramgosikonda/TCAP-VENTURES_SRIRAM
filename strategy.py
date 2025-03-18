import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt

class BollingerBandStrategy:

    def __init__(self, window=20, num_std=2.5, below_band_pct=0.01):

        self.window = window
        self.num_std = num_std
        self.below_band_pct = below_band_pct
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        
    def calculate_bands(self, prices):
        """Calculate Bollinger Bands"""
        rolling_mean = prices.rolling(window=self.window).mean()
        rolling_std = prices.rolling(window=self.window).std()
        
        self.upper_band = rolling_mean + (rolling_std * self.num_std)
        self.lower_band = rolling_mean - (rolling_std * self.num_std)
        
        return self.upper_band, self.lower_band
        
    def generate_signals(self, prices):
        """Generate buy/sell signals based on Bollinger Band strategy"""
        signals = pd.DataFrame(index=prices.index)
        signals['price'] = prices
        
        # Calculate bands
        self.calculate_bands(prices)
        
        # Initialize signals
        signals['signal'] = 0
        
        # Buy signal: Price falls 3% below lower band
        buy_condition = prices < (self.lower_band * (1 - self.below_band_pct))
        signals.loc[buy_condition, 'signal'] = 1
        if buy_condition.any():
            self.logger.info(f"Buy signal triggered at {prices[buy_condition].index[0]}")
        
        # Sell signal: Price touches upper band
        sell_condition = prices >= self.upper_band
        signals.loc[sell_condition, 'signal'] = -1
        if sell_condition.any():
            self.logger.info(f"Sell signal triggered at {prices[sell_condition].index[0]}")

        
        return signals
        
    def save_signals(self, signals, filepath='signals.csv'):
        """Save generated signals to CSV file for inspection"""
        signals.to_csv(filepath)
        self.logger.info(f"Saved signals to {filepath}")
        
    def plot_bands(self, prices, filepath='bollinger_bands.png'):
        """Plot Bollinger Bands with price data"""
        plt.figure(figsize=(12, 6))
        plt.plot(prices, label='Price')
        plt.plot(self.upper_band, label='Upper Band')
        plt.plot(self.lower_band, label='Lower Band')
        plt.title('Bollinger Bands')
        plt.legend()
        plt.savefig(filepath)
        self.logger.info(f"Saved Bollinger Bands plot to {filepath}")
        plt.close()

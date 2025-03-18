import pandas as pd
from strategy import BollingerBandStrategy

class Backtest:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.strategy = BollingerBandStrategy()
        
    def run(self):
        # Prepare data
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data.set_index('timestamp', inplace=True)
        
        # Generate signals
        signals = self.strategy.generate_signals(self.data['close'])
        
        # Save signals and plot bands for inspection
        self.strategy.save_signals(signals)
        self.strategy.plot_bands(self.data['close'])

        
        # Initialize trade tracking
        trades = []
        in_position = False
        entry_price = None
        entry_time = None
        
        # Simulate trades and log signals
        self.save_signals(signals)  # Log generated signals for inspection

        for timestamp, row in signals.iterrows():
            if not in_position and row['signal'] == 1:  # Buy signal
                in_position = True
                entry_price = row['price']
                entry_time = timestamp
                
            elif in_position and row['signal'] == -1:  # Sell signal
                in_position = False
                exit_price = row['price']
                exit_time = timestamp
                
                # Calculate trade metrics
                profit_pct = ((exit_price - entry_price) / entry_price) * 100
                
                # Record trade
                trades.append({
                    'token': 'BTCUSDT',
                    'date_in': entry_time,
                    'buy_price': entry_price,
                    'date_out': exit_time,
                    'sell_price': exit_price,
                    'profit_percentage': profit_pct
                })
        
        # Convert trades to DataFrame
        self.trades_df = pd.DataFrame(trades)
        
        if len(self.trades_df) == 0:
            print("Warning: No trades were generated. Details:")
            print(f"- Strategy Parameters: window={self.strategy.window}, num_std={self.strategy.num_std}, below_band_pct={self.strategy.below_band_pct}")
            print(f"- Price Range: {self.data['close'].min():.2f} to {self.data['close'].max():.2f}")
            print("Suggestions:")
            print("- Try adjusting below_band_pct to a smaller value")
            print("- Consider increasing num_std to make bands wider")
            print("- Verify if price data has sufficient volatility")

            
        return self.trades_df

    
    def calculate_metrics(self):
        """Calculate performance metrics"""
        metrics = {}
        
        if not self.trades_df.empty:
            # Basic metrics
            metrics['total_trades'] = len(self.trades_df)
            metrics['winning_trades'] = len(self.trades_df[self.trades_df['profit_percentage'] > 0])
            metrics['losing_trades'] = len(self.trades_df[self.trades_df['profit_percentage'] <= 0])
            metrics['win_rate'] = metrics['winning_trades'] / metrics['total_trades'] if metrics['total_trades'] > 0 else 0
            
            # Profit metrics
            metrics['total_profit'] = self.trades_df['profit_percentage'].sum()
            metrics['avg_profit'] = self.trades_df['profit_percentage'].mean()
            metrics['max_profit'] = self.trades_df['profit_percentage'].max()
            metrics['min_profit'] = self.trades_df['profit_percentage'].min()
            
            # Risk metrics
            metrics['max_drawdown'] = (self.trades_df['profit_percentage'].cumsum().min())
            
            # Strategy parameters
            metrics['strategy_window'] = self.strategy.window
            metrics['strategy_num_std'] = self.strategy.num_std
            metrics['strategy_below_band_pct'] = self.strategy.below_band_pct
            
        return metrics

    def display_metrics(self):
        """Display performance metrics in a readable format"""
        metrics = self.calculate_metrics()
        
        if not metrics:
            print("No metrics available - no trades were executed")
            return
            
        print("\n=== Backtest Performance Metrics ===")
        print(f"Total Trades: {metrics['total_trades']}")
        print(f"Winning Trades: {metrics['winning_trades']}")
        print(f"Losing Trades: {metrics['losing_trades']}")
        print(f"Win Rate: {metrics['win_rate']:.2%}")
        print(f"\nTotal Profit: {metrics['total_profit']:.2f}%")
        print(f"Average Profit per Trade: {metrics['avg_profit']:.2f}%")
        print(f"Maximum Profit: {metrics['max_profit']:.2f}%")
        print(f"Minimum Profit: {metrics['min_profit']:.2f}%")
        print(f"\nMaximum Drawdown: {metrics['max_drawdown']:.2f}%")
        print("\nStrategy Parameters:")
        print(f"- Window: {metrics['strategy_window']}")
        print(f"- Number of Std Devs: {metrics['strategy_num_std']}")
        print(f"- Below Band Percentage: {metrics['strategy_below_band_pct']}")

    def save_results(self, output_path):
        """Save trade results to CSV with error handling"""
        try:
            if self.trades_df.empty:
                print(f"Warning: No trades to save. Empty DataFrame will be written to {output_path}")
            
            # Add strategy parameters as metadata
            params = {
                'strategy_window': self.strategy.window,
                'strategy_num_std': self.strategy.num_std,
                'strategy_below_band_pct': self.strategy.below_band_pct
            }
            
            # Convert params to DataFrame and save as first row
            params_df = pd.DataFrame([params])
            params_df.to_csv(output_path, index=False, mode='w')
            
            # Append trade results
            self.trades_df.to_csv(output_path, index=False, mode='a', header=not params_df.empty)

            
            print(f"Successfully saved results to {output_path}")
            
        except Exception as e:
            print(f"Error saving results to {output_path}: {str(e)}")

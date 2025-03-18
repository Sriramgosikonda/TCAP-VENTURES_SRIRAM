# TCAP-VENTURES_SRIRAM

This project implements a trading strategy utilizing Bollinger Bands to identify potential buy and sell signals in stock market data. The strategy is backtested to evaluate its performance over historical data.

## Project Structure

- `app.py`: Main application script that orchestrates data processing, strategy execution, and result visualization.
- `backtest.py`: Contains functions and classes responsible for backtesting the trading strategy.
- `strategy.py`: Defines the trading strategy based on Bollinger Bands.
- `sriram.py`: Additional script for data analysis or utility functions.
- `data/`: Directory containing input data files used for backtesting.
- `templates/`: Directory for HTML templates, possibly used for generating reports or dashboards.
- `bollinger_bands.png`: Image illustrating the Bollinger Bands for a particular stock.
- `output window.mp4`: Video demonstrating the application's output or user interface.
- `signals.csv`: CSV file listing the buy and sell signals generated by the strategy.
- `trade_results.csv`: CSV file summarizing the results of executed trades during backtesting.

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- flask (if a web interface is implemented)

Install the required packages using:

```bash
pip install pandas numpy matplotlib flask

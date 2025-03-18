from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def show_trades():
    # Load trade results
    trades = pd.read_csv('trade_results.csv')
    
    # Convert to HTML table
    trades_html = trades.to_html(classes='table table-striped', index=False)
    
    return render_template('trades.html', trades_table=trades_html)

if __name__ == '__main__':
    app.run(debug=True)

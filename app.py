from flask import Flask, request, render_template_string
import yfinance as yf
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/stock/<symbol>')
def stock_chart(symbol):
    try:
        symbol = symbol.title()  # Accepts names like "Apple"
        symbol_map = {
            "Apple": "AAPL",
            "Google": "GOOG",
            "Microsoft": "MSFT",
            "Tesla": "TSLA",
            "Amazon": "AMZN"
        }

        if symbol not in symbol_map:
            return f"<h2>Error: Asset '{symbol}' not found.</h2>"

        ticker = symbol_map[symbol]
        data = yf.download(ticker, period="6mo")
        data["SMA20"] = data["Close"].rolling(window=20).mean()
        data["SMA50"] = data["Close"].rolling(window=50).mean()

        fig, ax = plt.subplots()
        ax.plot(data["Close"], label="Price")
        ax.plot(data["SMA20"], label="SMA20")
        ax.plot(data["SMA50"], label="SMA50")
        ax.set_title(f"{symbol} - Moving Average Crossover")
        ax.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode()
        buf.close()

        html = f"""
        <html><body>
        <h2>Chart for {symbol}</h2>
        <img src="data:image/png;base64,{img_base64}" />
        </body></html>
        """
        return html
    except Exception as e:
        return f"<h2>Error: {str(e)}</h2>"

if __name__ == '__main__':
    app.run(debug=True)
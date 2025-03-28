
import streamlit as st
import requests
import yfinance as yf

# Define asset categories and their correct symbols
assets = {
    'Cryptocurrencies': {
        'Bitcoin (BTC)': 'BTCUSDT',
        'Ethereum (ETH)': 'ETHUSDT',
        'XRP': 'XRPUSDT',
        'Solana (SOL)': 'SOLUSDT',
        'Cardano (ADA)': 'ADAUSDT',
        'Chainlink (LINK)': 'LINKUSDT',
        'Curve (CRV)': 'CRVUSDT',
        'Convex (CVX)': 'CVXUSDT',
        'Sui (SUI)': 'SUIUSDT',
        'Fartcoin': 'FARTUSDT',
        'Ondo (ONDO)': 'ONDOUSDT'
    },
    'Stocks': {
        'Tesla (TSLA)': 'TSLA',
        'NVIDIA (NVDA)': 'NVDA'
    },
    'Commodities': {
        'Gold (XAU)': 'GLD'  # Using GLD ETF
    }
}

# Live price fetchers
def get_crypto_price(binance_symbol):
    try:
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={binance_symbol}'
        response = requests.get(url)
        data = response.json()
        return float(data['price'])
    except:
        return None

def get_stock_price(yahoo_symbol):
    try:
        stock = yf.Ticker(yahoo_symbol)
        data = stock.history(period='1d')
        return data['Close'].iloc[-1]
    except:
        return None

# Trade risk calculation
def calculate_trade_risk(account_size_gbp, leverage, risk_percent, entry_price, stop_loss_price):
    position_size = account_size_gbp * leverage
    risk_amount = account_size_gbp * (risk_percent / 100)
    stop_loss_distance = abs(entry_price - stop_loss_price)
    stop_loss_pct = (stop_loss_distance / entry_price) * 100
    max_allowed_stop_pct = (risk_amount / position_size) * 100

    result = {
        "Account Size (Â£)": account_size_gbp,
        "Leverage": leverage,
        "Risk % of Account": risk_percent,
        "Risk Amount (Â£)": round(risk_amount, 2),
        "Entry Price": entry_price,
        "Stop-Loss Price": stop_loss_price,
        "Stop-Loss Distance (Â£)": round(stop_loss_distance, 2),
        "Stop-Loss %": round(stop_loss_pct, 4),
        "Position Size (Â£)": round(position_size, 2),
        "Max Allowed SL %": round(max_allowed_stop_pct, 4),
        "Within Risk?": stop_loss_pct <= max_allowed_stop_pct
    }

    return result

# Streamlit UI
st.title("Leverage Risk Calculator with Live Prices")

# Select category and asset
category = st.selectbox("Select Asset Category", list(assets.keys()))
asset_name = st.selectbox("Select Asset", list(assets[category].keys()))
symbol = assets[category][asset_name]

# Fetch live price
if category == "Cryptocurrencies":
    price = get_crypto_price(symbol)
else:
    price = get_stock_price(symbol)

if price:
    st.success(f"Live price for {asset_name}: ${price:.2f}")
else:
    st.warning(f"Live price for {asset_name} not available. Enter manually.")

# User inputs
account_size = st.number_input("Account Size (Â£)", value=500)
leverage = st.number_input("Leverage", value=20)
risk_percent = st.number_input("Risk % of Account", min_value=0.0, max_value=100.0, value=2.0)
entry_price = st.number_input("Entry Price", value=price if price else 0.0)
stop_loss_price = st.number_input("Stop-Loss Price", value=price * 0.98 if price else 0.0)

# Show results
if st.button("Calculate Risk"):
    trade = calculate_trade_risk(account_size, leverage, risk_percent, entry_price, stop_loss_price)
    st.subheader("Trade Summary")
    for key, value in trade.items():
        st.write(f"{key}: {value}")

import streamlit as st
import requests
import yfinance as yf

# CoinGecko ID mapping
coingecko_ids = {
    'Bitcoin (BTC)': 'bitcoin',
    'Ethereum (ETH)': 'ethereum',
    'XRP': 'ripple',
    'Solana (SOL)': 'solana',
    'Cardano (ADA)': 'cardano',
    'Chainlink (LINK)': 'chainlink',
    'Curve (CRV)': 'curve-dao-token',
    'Convex (CVX)': 'convex-finance',
    'Sui (SUI)': 'sui',
    'Fartcoin': 'fartcoin',
    'Ondo (ONDO)': 'ondo-finance'
}

assets = {
    'Cryptocurrencies': list(coingecko_ids.keys()),
    'Stocks': {
        'Tesla (TSLA)': 'TSLA',
        'NVIDIA (NVDA)': 'NVDA'
    },
    'Commodities': {
        'Gold (XAU)': 'GLD'
    }
}

def get_crypto_price_from_coingecko(name):
    try:
        coin_id = coingecko_ids.get(name)
        if not coin_id:
            raise ValueError("Unknown CoinGecko ID")
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data[coin_id]['usd']
    except Exception as e:
        st.error(f"CoinGecko API Error for {name}: {e}")
        return None

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period='1d')
        return data['Close'].iloc[-1]
    except Exception as e:
        st.error(f"Yahoo Finance Error for {symbol}: {e}")
        return None

def calculate_trade_risk(account_size_gbp, leverage, risk_percent, entry_price, stop_loss_price, take_profit_price):
    position_size = account_size_gbp * leverage
    risk_amount = account_size_gbp * (risk_percent / 100)

    stop_loss_distance = abs(entry_price - stop_loss_price)
    stop_loss_pct = (stop_loss_distance / entry_price) * 100
    total_loss_if_hit = position_size * (stop_loss_pct / 100)

    take_profit_distance = abs(take_profit_price - entry_price)
    potential_reward = position_size * (take_profit_distance / entry_price)
    rr_ratio = potential_reward / total_loss_if_hit if total_loss_if_hit else None

    max_allowed_stop_pct = (risk_amount / position_size) * 100

    result = {
        "Account Size (Â£)": account_size_gbp,
        "Leverage": leverage,
        "Risk % of Account": risk_percent,
        "Risk Amount (Â£)": round(risk_amount, 2),
        "Entry Price": entry_price,
        "Stop-Loss Price": stop_loss_price,
        "Take-Profit Price": take_profit_price,
        "Stop-Loss Distance (Â£)": round(stop_loss_distance, 2),
        "Take-Profit Distance (Â£)": round(take_profit_distance, 2),
        "Stop-Loss %": round(stop_loss_pct, 4),
        "Position Size (Â£)": round(position_size, 2),
        "Expected Loss if SL Hit (Â£)": round(total_loss_if_hit, 2),
        "Expected Reward if TP Hit (Â£)": round(potential_reward, 2),
        "Risk-Reward Ratio": round(rr_ratio, 2) if rr_ratio else "N/A",
        "Max Allowed SL %": round(max_allowed_stop_pct, 4),
        "Within Risk?": stop_loss_pct <= max_allowed_stop_pct
    }

    return result

# Streamlit UI
st.title("Leverage Risk Calculator with TP and R:R")

category = st.selectbox("Select Asset Category", list(assets.keys()))
if category == "Cryptocurrencies":
    asset_name = st.selectbox("Select Asset", assets[category])
    price = get_crypto_price_from_coingecko(asset_name)
else:
    asset_name = st.selectbox("Select Asset", list(assets[category].keys()))
    symbol = assets[category][asset_name]
    price = get_stock_price(symbol)

if price:
    st.success(f"Live price for {asset_name}: Â£{price:.2f}")
else:
    st.warning(f"Live price for {asset_name} not available. Enter manually.")

account_size = st.number_input("Account Size (Â£)", value=500)
leverage = st.number_input("Leverage", value=10)
risk_percent = st.number_input("Risk % of Account", min_value=0.0, max_value=100.0, value=1.0)
entry_price = st.number_input("Entry Price", value=price if price else 0.0)
stop_loss_price = st.number_input("Stop-Loss Price", value=price * 0.99 if price else 0.0)
take_profit_price = st.number_input("Take-Profit Price", value=price * 1.03 if price else 0.0)

if st.button("Calculate Risk"):
    trade = calculate_trade_risk(account_size, leverage, risk_percent, entry_price, stop_loss_price, take_profit_price)
    st.subheader("Trade Summary")
    for key, value in trade.items():
        st.write(f"{key}: Â£{value}" if "Â£" in key else f"{key}: {value}")
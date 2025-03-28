
import streamlit as st

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

st.title("Leverage Risk Calculator")

account_size = st.number_input("Account Size (Â£)", value=500)
leverage = st.number_input("Leverage", value=20)
risk_percent = st.number_input("Risk % of Account", min_value=0.0, max_value=100.0, value=2.0)
entry_price = st.number_input("Entry Price", value=85700.0)
stop_loss_price = st.number_input("Stop-Loss Price", value=84500.0)

if st.button("Calculate Risk"):
    trade = calculate_trade_risk(account_size, leverage, risk_percent, entry_price, stop_loss_price)
    for key, value in trade.items():
        st.write(f"{key}: {value}")

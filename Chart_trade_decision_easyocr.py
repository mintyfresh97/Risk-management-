
import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re

st.title("Chart Trade Decision (AI-Powered with EasyOCR)")

st.markdown("""
Upload a chart screenshot and this tool will scan for key levels (e.g. Fib 50%, 61.8%) and decide
if a trade meets your entry criteria.
""")

uploaded_file = st.file_uploader("Upload chart image", type=["png", "jpg", "jpeg"])

def extract_prices_with_easyocr(image):
    reader = easyocr.Reader(['en'], gpu=False)
    img_array = np.array(image)
    results = reader.readtext(img_array, detail=0)
    price_matches = re.findall(r"\b\d{1,5}(?:\.\d{1,4})?\b", " ".join(results))
    prices = sorted(set(float(p) for p in price_matches if float(p) > 0), reverse=True)
    return prices

def evaluate_trade_decision(prices):
    decision = "No Go"
    explanation = []

    for p in prices:
        if 0.5 <= p <= 0.618:
            decision = "Go"
            explanation.append(f"Fib zone detected: {p}")
        if 0.48 <= p <= 0.52:
            explanation.append(f"Near 50% Fib: {p}")
        if 0.6 <= p <= 0.63:
            explanation.append(f"Near 61.8% Fib: {p}")

    if not explanation:
        explanation.append("No valid fib zone found")

    return decision, explanation

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_column_width=True)

    with st.spinner("Analyzing chart..."):
        fib_prices = extract_prices_with_easyocr(image)
        decision, reasons = evaluate_trade_decision(fib_prices)

        st.subheader("Trade Decision")
        st.write(f"**{decision}**")
        st.write("Reasons:")
        for r in reasons:
            st.write(f"- {r}")

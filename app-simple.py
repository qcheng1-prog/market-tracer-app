import streamlit as st
import pandas as pd
import requests
import yfinance as yf

st.title("📈 Stock & Crypto Tracker")
ticker = st.sidebar.selectbox("Select Asset:", ["BTC-USD", "ETH-USD", "AAPL", "NVDA"])

# Fetch data using yfinance
data = yf.Ticker(ticker).history(period="1mo")

if not data.empty:
    st.metric(label=f"Current {ticker} Price", value=f"${data['Close'].iloc[-1]:,.2f}")
    st.line_chart(data["Close"])
else:
    st.warning("API rate limit hit. Showing cached/fallback data.")
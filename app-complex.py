import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Multi-Asset Market Tracker", page_icon="📈", layout="wide")

st.title("📈 Multi-Asset Stock & Crypto Comparison")
st.write("Compare multiple assets simultaneously using live market data from `yfinance`.")

# Categorized Assets
ASSETS = {
    "Cryptocurrencies": ["BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD"],
    "Big Tech": ["AAPL", "NVDA", "MSFT", "GOOGL", "AMZN", "TSLA"],
    "Market Indices": ["^GSPC", "^IXIC", "^DJI"],
    "Commodities & Forex": ["GC=F", "CL=F", "EURUSD=X"]
}

all_assets = [item for sublist in ASSETS.values() for item in sublist]

# Sidebar Controls
st.sidebar.header("Chart Settings")

# Multiselect widget for assets
selected_tickers = st.sidebar.multiselect(
    "Select Assets to Compare:",
    options=all_assets,
    default=["BTC-USD", "NVDA", "AAPL"]  # Defaults to 3 tickers
)

time_period = st.sidebar.selectbox(
    "Select Time Horizon:",
    options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
    index=2  # Default to 1mo
)

if selected_tickers:
    # Fetch data for all selected tickers at once
    with st.spinner("Fetching market data..."):
        raw_data = yf.download(selected_tickers, period=time_period)["Close"]

    # If only 1 ticker selected, convert Series to DataFrame
    if isinstance(raw_data, pd.Series):
        df_close = raw_data.to_frame(name=selected_tickers[0])
    else:
        df_close = raw_data

    if not df_close.empty:
        # --- SECTION 1: Metrics Row ---
        st.subheader("Current Performance Summary")
        cols = st.columns(len(selected_tickers))
        
        for idx, ticker in enumerate(selected_tickers):
            if ticker in df_close.columns and not df_close[ticker].dropna().empty:
                series = df_close[ticker].dropna()
                current_price = series.iloc[-1]
                start_price = series.iloc[0]
                price_change = current_price - start_price
                pct_change = (price_change / start_price) * 100
                
                cols[idx].metric(
                    label=ticker,
                    value=f"${current_price:,.2f}",
                    delta=f"{price_change:+,.2f} ({pct_change:+.2f}%)"
                )

        st.markdown("---")

        # --- SECTION 2: Combined Normalized Chart ---
        st.subheader(f"Relative Performance Comparison (% Change over {time_period})")
        st.caption("Prices are normalized to start at 0% so assets with different price scales can be compared directly.")
        
        # Calculate % return from day 1 for direct overlay comparison
        normalized_df = ((df_close / df_close.iloc[0]) - 1) * 100
        st.line_chart(normalized_df)

        st.markdown("---")

        # --- SECTION 3: Individual Unscaled Plots ---
        st.subheader("Individual Price Charts (Actual Prices in USD)")
        
        # Display individual charts in a 2-column layout
        grid_cols = st.columns(2)
        for idx, ticker in enumerate(selected_tickers):
            if ticker in df_close.columns and not df_close[ticker].dropna().empty:
                with grid_cols[idx % 2]:
                    st.write(f"**{ticker}**")
                    st.line_chart(df_close[ticker].dropna())

        # Raw Data Expander
        with st.expander("View Raw Price Data Table"):
            st.dataframe(df_close.sort_index(ascending=False))
    else:
        st.error("Unable to load data for the selected assets. Please try different tickers.")
else:
    st.info("Please select at least one asset from the sidebar to display charts.")

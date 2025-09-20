import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil import parser as dtparser
import yfinance as yf

st.set_page_config(page_title="Dividend Yield Calculator", page_icon="💸", layout="centered")

st.title("💸 Dividend Yield Calculator (Yahoo Finance)")
st.caption("Enter a stock/ETF ticker and your investment date. We'll fetch Yahoo Finance dividends, "
           "count only those where your investment date is strictly **before** the ex-dividend date, "
           "and compute **yield on cost**.")

@st.cache_data(show_spinner=False, ttl=3600)
def fetch_prices(ticker: str, start_dt: date, end_dt: date) -> pd.DataFrame:
    df = yf.download(ticker, start=start_dt.isoformat(), end=(end_dt + timedelta(days=1)).isoformat(),
                     auto_adjust=True, progress=False)
    return df

@st.cache_data(show_spinner=False, ttl=3600)
def fetch_dividends(ticker: str) -> pd.DataFrame:
    t = yf.Ticker(ticker)
    s = t.dividends  # Series with ex-dividend Date index (UTC tz)
    if s is None or len(s) == 0:
        return pd.DataFrame(columns=["ex_date", "dividend"])
    s.index = pd.to_datetime(s.index).date
    df = s.reset_index()
    df.columns = ["ex_date", "dividend"]
    return df

def first_trading_price_on_or_after(df_prices: pd.DataFrame, start_dt: date):
    if df_prices.empty:
        return None, None
    tmp = df_prices.reset_index()
    tmp["DateOnly"] = pd.to_datetime(tmp["Date"]).dt.date
    row = tmp.loc[tmp["DateOnly"] >= start_dt]
    if row.empty:
        return None, None
    r0 = row.iloc[0]
    return r0["DateOnly"], float(r0["Close"].iloc[0])

def compute_yield_on_cost(ticker: str, invest_dt: date, end_dt: date):
    # get prices: search a small window before invest_dt to ensure availability
    px = fetch_prices(ticker, invest_dt - timedelta(days=7), end_dt + timedelta(days=1))
    price_date, purchase_price = first_trading_price_on_or_after(px, invest_dt)
    if purchase_price is None:
        raise ValueError(f"No trading day on/after {invest_dt} for {ticker}.")
    divs = fetch_dividends(ticker)
    if not divs.empty:
        mask = (divs["ex_date"] > invest_dt) & (divs["ex_date"] <= end_dt)
        divs = divs.loc[mask].sort_values("ex_date").reset_index(drop=True)
    total_divs = float(divs["dividend"].sum()) if not divs.empty else 0.0
    yoc = total_divs / purchase_price if purchase_price > 0 else float("nan")
    return purchase_price, price_date, divs, total_divs, yoc

with st.form("inputs"):
    default_ticker = st.session_state.get("ticker", "AAPL")
    ticker = st.text_input("Ticker", value=default_ticker, placeholder="e.g., AAPL, MSFT, TSLA").upper().strip()
    col1, col2 = st.columns(2)
    invest_date = col1.date_input("Investment date", value=date(2020,1,2), min_value=date(1980,1,1), max_value=date.today())
    end_date = col2.date_input("End date (dividend window end)", value=date.today(), min_value=invest_date, max_value=date.today())
    submitted = st.form_submit_button("Calculate")

if submitted:
    if not ticker:
        st.error("Please enter a ticker.")
    else:
        try:
            with st.spinner("Fetching data from Yahoo Finance…"):
                purchase_price, price_date, divs, total_divs, yoc = compute_yield_on_cost(ticker, invest_date, end_date)

            st.success("Done!")
            st.subheader("Results")
            m1, m2, m3 = st.columns(3)
            m1.metric("Purchase price per share", f"${purchase_price:,.4f}", help=f"On the first trading day on/after {price_date}")
            m2.metric("Total dividends per share", f"${total_divs:,.4f}", help="Sum of dividends with ex-date strictly after invest date and up to the end date")
            m3.metric("Yield on cost", f"{yoc:.2%}", help="Dividends per share ÷ purchase price")

            st.markdown("---")
            st.subheader("Dividend breakdown (ex-dividend dates)")
            if divs.empty:
                st.info("No dividends in the chosen window.")
            else:
                st.dataframe(divs, use_container_width=True, hide_index=True)
                csv = divs.to_csv(index=False).encode("utf-8")
                st.download_button("Download CSV", data=csv, file_name=f"{ticker}_dividends_{invest_date}_{end_date}.csv", mime="text/csv")

            st.markdown("---")
            st.caption("Notes: Uses Yahoo Finance via yfinance. Dividends counted only if your investment date is strictly **before** the ex-dividend date. "
                       "Purchase price uses adjusted close of the first trading day on/after your investment date.")

            st.session_state["ticker"] = ticker

        except Exception as e:
            st.error(str(e))
            st.stop()

st.markdown("")
st.markdown("> Tip: To estimate **forward yield**, multiply the most recent dividend by its frequency (e.g., ×4 for quarterly) and divide by current price.")

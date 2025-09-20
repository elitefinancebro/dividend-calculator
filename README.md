# Dividend Yield Calculator (Web App)

A simple Streamlit web app that:
- Fetches dividend history and prices from Yahoo Finance (via `yfinance`)
- Counts a dividend only if you **owned the stock before the ex-dividend date**
- Uses the first trading day **on/after** your investment date for purchase price
- Computes **total dividends per share** and **yield on cost**

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL that Streamlit prints (usually http://localhost:8501).

## Notes
- Data source: Yahoo Finance via `yfinance`
- Ex-date logic: dividend counted only if ex-date `>` investment date
- Purchase price: adjusted close on first trading day on/after your investment date
# dividend-calculator

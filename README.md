
# Dividend Calculator

A simple, accurate **dividend yield & cash-flow calculator** that pulls historical dividend events, checks **ex-dividend date** eligibility based on your **purchase date**, and computes realized dividend income, yield, and optional DRIP effects. Built with **Streamlit** for a clean, interactive UI.

**Live App:** [https://dividend-calculator-by-ashish.streamlit.app](https://dividend-calculator-by-ashish.streamlit.app)

---

## ✨ Features

* **Ticker + Purchase Date input**: calculates dividends collected only if the position was held **before the ex-dividend date**.
* **Accurate cashflows**: sums paid dividends over the selected holding period.
* **Dividend yield metrics**: absolute dividend income, simple dividend yield, and yield-on-cost.
* **Clear audit trail**: shows all dividend events used in the calculation (ex-date, pay date, amount).
* **Fast, friendly UI**: Streamlit app with instant recalculation on input change.

> **Use case:** “If I bought `AAPL` on 2022-01-02, which dividends would I have actually collected, and what’s my dividend yield or yield-on-cost?”

---

## 🚀 Quick Start

### Prerequisites

* Python 3.10+ recommended
* pip (or uv/pdm/poetry if you prefer)

### Setup

```bash
# 1) Clone
git clone https://github.com/elitefinancebro/dividend-calculator.git
cd dividend-calculator

# 2) (Optional) Create a virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run locally
streamlit run app.py
```

Then open the local URL that Streamlit prints (usually [http://localhost:8501](http://localhost:8501)).

---

## 🖥️ Usage

1. Open the **[live app](https://dividend-calculator-by-ashish.streamlit.app)** or run locally.
2. Enter:

   * **Ticker** (e.g., `AAPL`, `MSFT`, `V`).
   * **Investment (purchase) date**.
   * **(Optional) Shares / Initial investment**, and **DRIP** toggle if supported.
3. Click **Calculate** to view:

   * **Collected dividends** (events where ex-date ≥ purchase date logic is satisfied).
   * **Total dividend income**.
   * **Dividend yield / yield-on-cost**.
   * **(Optional) DRIP results** and event table.

---

## 📦 Project Structure

> Adjust this section if your filenames differ.

```
dividend-calculator/
├─ app.py                 # Streamlit UI entrypoint
├─ core/
│  ├─ dividends.py        # Fetch + filter dividend events (ex-div logic)
│  ├─ calculator.py       # Yield, cashflow, DRIP computations
│  └─ utils.py            # Helpers (date, formatting, caching)
├─ requirements.txt
├─ README.md
└─ LICENSE                # (Add your chosen license)
```

---

## ⚙️ Configuration

Most setups work without special config. If you use an API that needs keys:

* Create a `.env` file and read it in `app.py` (e.g., with `python-dotenv`).
* Example:

  ```
  DATA_API_KEY=your_key_here
  ```

---

## 📊 Data & Assumptions

* **Dividends**: Queried from a public market data library or API (e.g., Yahoo Finance via `yfinance`) that provides historical **ex-dividend dates** and **cash dividend amounts**.
* **Eligibility**: A dividend is counted only if the position existed **before** the **ex-dividend date** (standard market convention).
* **Corporate actions**: Basic handling assumed; complex actions (splits, special distributions, spin-offs) may require manual review.
* **DRIP**: If enabled, the model reinvests at (by default) close price on pay date or another chosen convention; results are approximations.

> **Note:** Real portfolios can include partial fills, taxes, FX, fees, and lot selection—these are out of scope for a simple calculator but can be added.

---

## 🧪 Testing (suggested)

```bash
# If you add tests with pytest
pip install -r requirements-dev.txt
pytest -q
```

Focus unit tests on:

* Ex-dividend eligibility logic
* Dividend summation across periods
* DRIP share accumulation math

---

## 🔧 Development Notes

* Cache expensive calls (e.g., price/dividend history) with `st.cache_data` or equivalent.
* Validate inputs (e.g., future dates, invalid tickers) and show clear error messages.
* Keep logic pure in `core/` modules; keep Streamlit code thin in `app.py`.

---

## 🗺️ Roadmap

* ✅ Base calculator (ticker + purchase date)
* ⏳ Add **cash vs. DRIP** side-by-side comparison
* ⏳ Add **period filters** (e.g., to date, custom end date)
* ⏳ Export **CSV** of dividend events & results
* ⏳ Multi-ticker portfolios

Feel free to open an issue or PR with suggestions.

---

## 🤝 Contributing

1. Fork the repo and create your branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -m "Add my feature"`
3. Push to branch: `git push origin feature/my-feature`
4. Open a Pull Request

Please keep PRs focused and include short test coverage where possible.



## 🙌 Acknowledgements

* The open-source Python & Streamlit community
* Public market data libraries/APIs (e.g., `yfinance`) for dividend histories

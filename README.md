# 🛒 Sales Automation Project (a humble beginner project)

Hi! this is a simple project i made to learn python and pandas.
basically it reads a csv with some sales, gets the dollar price from
a website, does a few analysis things, and saves everything to an
excel file. nothing fancy. i wrote comments everywhere so even
a total beginner can understand (thats me too lol).

---

## 📦 What this project does

1. **Reads** `data/sales_sample.csv` (1,000 fake e-commerce orders from 2024).
2. **Fetches** the USD → BRL exchange rate from a free API
   (Banco Central do Brasil, a.k.a. BCB).
3. **Cleans and enriches** the data (deletes empty rows, adds a `YearMonth`
   column, changes USD sales to BRL).
4. **Runs 4 analyses:**
   - **Basic statistics** per category (total, mean, median, max, min, count).
   - **Monthly summary** (orders, total sales, total profit, avg order value).
   - **Top 10 products** by total sales.
   - **Anomaly detection** (negative profit OR super high sales above the
     99% percentile).
5. **Writes** everything to `output/sales_report.xlsx` with:
   - 5 sheets (RawData, BasicStats, MonthlySummary, TopProducts, Anomalies)
   - Bold headers that stay at the top when scrolling
   - Columns auto-sized
   - 2 charts (monthly sales + top products) pasted next to their tables
6. **Saves** the 2 charts as png files in the `output/` folder too.

---

## 🗂️ Project structure

```
sales-automation-project/
├── README.md                  # the file you are reading right now
├── requirements.txt           # the libraries you need to install
├── main.py                    # the main script (this is the one!)
├── generate_sample_data.py    # makes the fake csv if you want fresh data
├── data/
│   └── sales_sample.csv       # the fake sales data (1,000 rows)
└── output/
    ├── sales_report.xlsx      # created when you run main.py
    ├── monthly_sales.png      # chart made by matplotlib
    └── top_products.png       # another chart made by matplotlib
```

---

## ✅ What you need

- **Python 3.9 or newer** (it worked on my python 3.10 and 3.12)
- **pip** (comes with python)
- internet (to get the exchange rate)

---

## 🚀 How to run it (step by step)

### Step 1 — Open a terminal

Windows: open **PowerShell** or **Command Prompt**.
Mac/Linux: open the **Terminal** app.

### Step 2 — Go to the project folder

```bash
cd path/to/sales-automation-project
```

(change the path to wherever you saved the project)

### Step 3 — (Optional but recommended) Create a virtual env

so the libraries dont mess with the rest of your computer.

```bash
# create it (only the first time)
python -m venv .venv

# activate it:
#   on Windows (PowerShell):
.venv\Scripts\Activate.ps1
#   on Mac/Linux:
source .venv/bin/activate
```

### Step 4 — Install the requirements

```bash
pip install -r requirements.txt
```

this installs `pandas`, `openpyxl`, `requests`, and `matplotlib`.

### Step 5 — Run the script

```bash
python main.py
```

you should see something like this:

```
============================================================
  SALES AUTOMATION PROJECT - STARTING
============================================================
[STEP] Reading CSV from: .../data/sales_sample.csv
       Loaded 1000 rows and 12 columns.
[STEP] Fetching USD -> BRL exchange rate from public API...
       Current USD -> BRL rate: 5.4321
[STEP] Cleaning and enriching the data...
       Data ready. Final shape: (1000, 14)
[STEP] Analysis 1: Basic statistics per category...
[STEP] Analysis 2: Sales grouped by month...
[STEP] Analysis 3: Top 10 products by sales...
[STEP] Analysis 4: Detecting anomalies...
[STEP] Writing Excel report to: .../output/sales_report.xlsx
[OK] Excel report written successfully.
============================================================
  DONE! Open the report at:
  .../output/sales_report.xlsx
============================================================
```

### Step 6 — Open the excel file

open `output/sales_report.xlsx` in Excel, Google Sheets, or LibreOffice.
you will see 5 tabs at the bottom, one for each analysis.

---

## 🔄 Want fresh fake data?

if you want a new batch of random sales, just run:

```bash
python generate_sample_data.py
```

it overwrites `data/sales_sample.csv` with 1,000 new fake orders.

---

## 🧠 The important stuff in main.py

| Concept              | Where to look in `main.py` | What it does                        |
| -------------------- | -------------------------- | ----------------------------------- |
| Read CSV             | `load_sales_data()`        | loads the csv into a dataframe      |
| Call an API          | `fetch_usd_brl_exchange_rate()` | gets the dollar price from BCB |
| Clean data           | `clean_and_enrich()`       | removes NaN rows and adds columns   |
| `groupby`            | `analyze_basic_stats()`    | groups by category and does math    |
| Date formatting      | `clean_and_enrich()`       | turns a date into `YYYY-MM`         |
| `quantile`           | `detect_anomalies()`       | finds the 99% percentile value      |
| ExcelWriter          | `write_excel_report()`     | writes multiple sheets to one file  |

---

## 🛠️ Cool things you could try next

1. **Add another analysis** — like sales per Region or per Channel.
2. **Add another chart** — the monthly and top-product charts are made with
   `matplotlib`; try a pie chart of sales per category.
3. **Schedule it** — use the `schedule` library to run it every monday.
4. **Email the report** — use `smtplib` to send the excel by email.
5. **Use real data** — hook it up to a real e-commerce api.

---

## 🎓 Academic project (not a real one!)

just to be clear: this is an **academic / educational project** made to learn
Python, pandas, matplotlib and the whole happy family. it is NOT meant for
real use, so:

- all data is **simulated / fake**, nothing is real and no one bought anything.
- it is not affiliated with or endorsed by any company or institution.
- do not plug your real sales data into this and use it to make business
  decisions, you have been warned lol.
- the code is kept simple and a bit sloppy on purpose so it is easy to read
  and learn from.

---

## ⚠️ Known limitations (its a beginner project, dont judge lol)

- the csv is fake data, not real sales.
- the exchange rate comes from the BCB PTAX api; if it is down the script
  falls back to a fixed rate of `5.00 BRL/USD` so we dont panic.
- no logs are saved to a file, everything just prints on the console.
- no unit tests. yeah i know.

---

## 📄 License

free to use for learning. no warranty. have fun! 🎉
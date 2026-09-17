# sales automation thing lol
# basically reads a csv, gets the dollar price, does some analysis, saves to excel
# i know my code is messy but it works lol

import os
import requests
import pandas as pd
from datetime import datetime
import matplotlib
matplotlib.use("Agg")   # so it works without a screen (for the charts)
import matplotlib.pyplot as plt
from openpyxl.styles import Font
from openpyxl.drawing.image import Image

# where the files are
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(PROJECT_ROOT, "data", "sales_sample.csv")
OUTPUT_XLSX = os.path.join(PROJECT_ROOT, "output", "sales_report.xlsx")
MONTHLY_CHART = os.path.join(PROJECT_ROOT, "output", "monthly_sales.png")
TOP_CHART = os.path.join(PROJECT_ROOT, "output", "top_products.png")


def load_sales_data(path):
    # just reads the csv
    print(f"[STEP] Reading CSV from: {path}")
    df = pd.read_csv(path, parse_dates=["OrderDate"])
    print(f"       Loaded {len(df)} rows and {len(df.columns)} columns.")
    return df


def fetch_usd_brl_rate():
    # gets the dollar price from a free api
    print("[STEP] Fetching USD -> BRL exchange rate from public API...")
    url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='01-01-2024'&@dataFinalCotacao='12-31-2024'&$top=1&$orderby=dataHoraCotacao%20desc&$format=json"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rate = float(data["value"][0]["cotacaoVenda"])
        print(f"       Current USD -> BRL rate: {rate:.4f}")
        return rate
    except Exception as error:
        # if it fails just use 5.00 so we dont break
        print(f"       [WARN] Could not fetch exchange rate: {error}")
        print(f"       [WARN] Falling back to a fixed rate of 5.00 BRL/USD.")
        return 5.00


def clean_data(df, rate):
    # clean some stuff and add columns
    print("[STEP] Cleaning and enriching the data...")

    # remove empty rows
    df = df.dropna()

    # month column like 2024-03
    df["YearMonth"] = df["OrderDate"].dt.strftime("%Y-%m")

    # sales in reais
    df["SalesBRL"] = (df["Sales"] * rate).round(2)

    # sort by date
    df = df.sort_values("OrderDate").reset_index(drop=True)

    print(f"       Data ready. Final shape: {df.shape}")
    return df


def basic_stats(df):
    # stats per category
    print("[STEP] Analysis 1: Basic statistics per category...")
    stats = df.groupby("Category")["Sales"].agg(
        TotalSales="sum",
        MeanSales="mean",
        MedianSales="median",
        MaxSales="max",
        MinSales="min",
        OrderCount="count",
    ).round(2)
    return stats.reset_index()


def monthly_summary(df):
    # sales per month
    print("[STEP] Analysis 2: Sales grouped by month...")
    monthly = df.groupby("YearMonth").agg(
        Orders=("OrderID", "count"),
        TotalSales=("Sales", "sum"),
        TotalProfit=("Profit", "sum"),
        AvgOrderValue=("Sales", "mean"),
    ).round(2)
    return monthly.reset_index()


def top_products(df, top_n=10):
    # best selling products
    print(f"[STEP] Analysis 3: Top {top_n} products by sales...")
    top = df.groupby("Product")["Sales"].sum().round(2)
    top = top.sort_values(ascending=False).head(top_n)
    return top.reset_index()


def find_anomalies(df):
    # weird stuff: lost money or huge orders
    print("[STEP] Analysis 4: Detecting anomalies...")

    anomalies_list = []

    # lost money on the order
    negative_profit = df[df["Profit"] < 0].copy()
    negative_profit["AnomalyType"] = "Negative Profit"
    anomalies_list.append(negative_profit)

    # higher than 99% of everything else
    threshold = df["Sales"].quantile(0.99)
    huge_sales = df[df["Sales"] > threshold].copy()
    huge_sales["AnomalyType"] = "Unusually High Sales"
    anomalies_list.append(huge_sales)

    # put them together
    anomalies = pd.concat(anomalies_list).reset_index(drop=True)

    # keep only whats useful
    anomalies = anomalies[
        ["OrderID", "OrderDate", "Product", "Sales", "Profit", "AnomalyType"]
    ]
    return anomalies


def make_monthly_chart(monthly, chart_path):
    # line chart of sales per month
    print(f"[STEP] Making monthly sales chart...")
    plt.figure(figsize=(10, 5))
    plt.plot(monthly["YearMonth"], monthly["TotalSales"], marker="o")
    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(chart_path, dpi=100)
    plt.close()


def make_top_chart(top, chart_path):
    # bar chart of the best selling products
    print(f"[STEP] Making top products chart...")
    plt.figure(figsize=(10, 5))
    plt.bar(top["Product"], top["Sales"], color="skyblue")
    plt.title("Top 10 Products by Sales")
    plt.xlabel("Product")
    plt.ylabel("Sales (USD)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(chart_path, dpi=100)
    plt.close()


def write_report(df, stats, monthly, top, anomalies, output_path,
                 monthly_chart_path, top_chart_path):
    # save everything to 1 excel file
    print(f"[STEP] Writing Excel report to: {output_path}")

    # make the output folder if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="RawData", index=False)
        stats.to_excel(writer, sheet_name="BasicStats", index=False)
        monthly.to_excel(writer, sheet_name="MonthlySummary", index=False)
        top.to_excel(writer, sheet_name="TopProducts", index=False)
        anomalies.to_excel(writer, sheet_name="Anomalies", index=False)

        # put the charts next to their tables
        worksheet = writer.sheets["MonthlySummary"]
        worksheet.add_image(Image(monthly_chart_path), "G2")

        worksheet = writer.sheets["TopProducts"]
        worksheet.add_image(Image(top_chart_path), "E2")

        # make headers bold and freeze first row
        for sheet_name, worksheet in writer.sheets.items():
            for col_idx in range(1, worksheet.max_column + 1):
                cell = worksheet.cell(row=1, column=col_idx)
                old_font = cell.font
                cell.font = Font(
                    name=old_font.name,
                    size=old_font.size,
                    bold=True,
                    italic=old_font.italic,
                    color=old_font.color,
                )

            worksheet.freeze_panes = "A2"

            # resize columns so they fit
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        cell_len = len(str(cell.value))
                        if cell_len > max_length:
                            max_length = cell_len
                    except Exception:
                        pass
                worksheet.column_dimensions[column_letter].width = max_length + 2

    print("[OK] Excel report written successfully.")


def main():
    print("=" * 60)
    print("  SALES AUTOMATION PROJECT - STARTING")
    print("=" * 60)

    # do everything in order
    df = load_sales_data(INPUT_CSV)
    rate = fetch_usd_brl_rate()
    df = clean_data(df, rate)
    stats = basic_stats(df)
    monthly = monthly_summary(df)
    top = top_products(df, top_n=10)
    anomalies = find_anomalies(df)

    # make the charts
    make_monthly_chart(monthly, MONTHLY_CHART)
    make_top_chart(top, TOP_CHART)

    write_report(df, stats, monthly, top, anomalies, OUTPUT_XLSX,
                 MONTHLY_CHART, TOP_CHART)

    print("=" * 60)
    print("  DONE! Open the report at:")
    print(f"  {OUTPUT_XLSX}")
    print("=" * 60)


if __name__ == "__main__":
    main()
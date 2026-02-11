# Project - 2 Expense Tracker CLI

import sqlite3
import argparse
import csv
from datetime import datetime
import matplotlib.pyplot as plt

DB_NAME = "expenses.db"


# ----------------------------
# Create database and table
# ----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            type TEXT,
            amount REAL
        )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# Add transaction
# ----------------------------
def add_transaction(date, category, t_type, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, category, type, amount)
        VALUES (?, ?, ?, ?)
    """, (date, category, t_type, amount))

    conn.commit()
    conn.close()

    print("Transaction added successfully.")


# ----------------------------
# Monthly summary
# ----------------------------
def monthly_summary(month):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, SUM(amount)
        FROM transactions
        WHERE strftime('%Y-%m', date) = ?
        GROUP BY type
    """, (month,))

    results = cursor.fetchall()
    conn.close()

    income = 0
    expense = 0

    for r in results:
        if r[0] == "income":
            income = r[1]
        elif r[0] == "expense":
            expense = r[1]

    balance = income - expense

    print(f"\nSummary for {month}")
    print(f"Total Income : {income}")
    print(f"Total Expense: {expense}")
    print(f"Balance      : {balance}")


# ----------------------------
# Export to CSV
# ----------------------------
def export_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT date, category, type, amount FROM transactions")
    rows = cursor.fetchall()
    conn.close()

    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Type", "Amount"])
        writer.writerows(rows)

    print("Exported to expenses.csv")


# ----------------------------
# Generate chart
# ----------------------------
def generate_chart(month):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type='expense' AND strftime('%Y-%m', date)=?
        GROUP BY category
    """, (month,))

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No expense data for this month.")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title(f"Expense Distribution - {month}")
    plt.savefig("expense_chart.png")
    plt.close()

    print("Chart saved as expense_chart.png")


# ----------------------------
# Main CLI
# ----------------------------
def main():
    init_db()

    parser = argparse.ArgumentParser(description="Expense Tracker CLI")

    parser.add_argument("--add", action="store_true", help="Add transaction")
    parser.add_argument("--date", help="Date (YYYY-MM-DD)")
    parser.add_argument("--category", help="Category")
    parser.add_argument("--type", choices=["income", "expense"], help="Type")
    parser.add_argument("--amount", type=float, help="Amount")

    parser.add_argument("--summary", help="Monthly summary (YYYY-MM)")
    parser.add_argument("--export", action="store_true", help="Export to CSV")
    parser.add_argument("--chart", help="Generate expense chart (YYYY-MM)")

    args = parser.parse_args()

    if args.add:
        if not all([args.date, args.category, args.type, args.amount]):
            print("Please provide --date --category --type --amount")
            return

        add_transaction(args.date, args.category, args.type, args.amount)

    elif args.summary:
        monthly_summary(args.summary)

    elif args.export:
        export_csv()

    elif args.chart:
        generate_chart(args.chart)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

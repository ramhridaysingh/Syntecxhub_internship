# Project - 1 News Aggregator CLI

import requests
import json
import sqlite3
import csv
import argparse

# 🔑 PASTE YOUR REAL API KEY HERE
API_KEY = "9f8d7c6b5a4e3d2c1abcd123456"

BASE_URL = "https://newsapi.org/v2/everything"


def fetch_news(keyword=None, source=None, from_date=None):
    if API_KEY == "PASTE_YOUR_REAL_API_KEY_HERE" or not API_KEY:
        print("Error: Please paste your real API key inside the code.")
        return []

    params = {
        "apiKey": API_KEY,
        "q": keyword if keyword else "news",
        "sources": source,
        "from": from_date,
        "language": "en",
        "pageSize": 50
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print("Error fetching news:", data.get("message"))
        return []

    return data.get("articles", [])


def remove_duplicates(articles):
    seen = set()
    unique = []

    for article in articles:
        title = article.get("title")
        if title and title not in seen:
            seen.add(title)
            unique.append(article)

    return unique


def save_to_json(articles):
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4)
    print("Saved to news.json")


def save_to_sqlite(articles):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            source TEXT,
            published_at TEXT,
            url TEXT
        )
    """)

    for article in articles:
        cursor.execute("""
            INSERT INTO news (title, source, published_at, url)
            VALUES (?, ?, ?, ?)
        """, (
            article.get("title"),
            article.get("source", {}).get("name"),
            article.get("publishedAt"),
            article.get("url")
        ))

    conn.commit()
    conn.close()
    print("Saved to news.db")


def export_to_csv(articles):
    with open("news.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Source", "Published At", "URL"])

        for article in articles:
            writer.writerow([
                article.get("title"),
                article.get("source", {}).get("name"),
                article.get("publishedAt"),
                article.get("url")
            ])

    print("Exported to news.csv")


def main():
    parser = argparse.ArgumentParser(description="Simple News Aggregator CLI")
    parser.add_argument("--keyword", help="Filter by keyword")
    parser.add_argument("--source", help="Filter by source")
    parser.add_argument("--date", help="Filter by date (YYYY-MM-DD)")
    parser.add_argument("--export", help="Export format (csv)")

    args = parser.parse_args()

    print("Fetching news...")
    articles = fetch_news(args.keyword, args.source, args.date)

    if not articles:
        print("No articles found.")
        return

    articles = remove_duplicates(articles)

    save_to_json(articles)
    save_to_sqlite(articles)

    if args.export == "csv":
        export_to_csv(articles)

    print("Total Articles:", len(articles))


if __name__ == "__main__":
    main()

              # Project-2:Web Scraper for Headlines

# File : Headline_Scraper.py
import requests
from bs4 import BeautifulSoup
import json
import csv
import time


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Simple Headline Scraper)"
}


def fetch_headlines(url, keyword=None):
    headlines = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Example: generic <a> tags used for headlines
        for tag in soup.find_all("a"):
            title = tag.get_text(strip=True)
            link = tag.get("href")

            if not title or not link:
                continue

            if keyword and keyword.lower() not in title.lower():
                continue

            if link.startswith("/"):
                link = url + link

            headlines.append({
                "title": title,
                "url": link,
                "time": "N/A"
            })

    except requests.exceptions.RequestException as e:
        print("❌ Error fetching website:", e)

    return headlines


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"✅ Data saved to {filename}")


def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "url", "time"])
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Data saved to {filename}")


    # ---------- Main Function ----------
def main():
    print("📰 Web Headline Scraper")

    url = input("Enter news website URL: ")
    keyword = input("Filter by keyword (press Enter to skip): ")

    print("Fetching headlines... Please wait")
    time.sleep(2)   # polite delay

    headlines = fetch_headlines(url, keyword if keyword else None)

    if not headlines:
        print("No headlines found.")
        return

    for i, news in enumerate(headlines, start=1):
        print(f"\n{i}. {news['title']}")
        print(f"   Link: {news['url']}")

    choice = input("\nSave output as (1) JSON or (2) CSV? ")

    if choice == "1":
        save_to_json(headlines, "headlines.json")
    elif choice == "2":
        save_to_csv(headlines, "headlines.csv")
    else:
        print("Invalid choice. Data not saved.")


# Run script
main()



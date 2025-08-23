import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv

# 🔧 Define site-specific selectors
SELECTORS = {
    "newegg.com": ".product-inventory",
    "example.com": ".stock-status",  # Add more as needed
}

def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")

def get_stock_status(url):
    domain = get_domain(url)
    selector = SELECTORS.get(domain)

    if not selector:
        return "Selector not defined"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else "Not found"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    with open("urls.txt") as f:
        urls = [line.strip() for line in f if line.strip()]

    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Stock Status"])

        for url in urls:
            status = get_stock_status(url)
            writer.writerow([url, status])
            print(f"{url} → {status}")

if __name__ == "__main__":
    main()

import requests
import pandas as pd
from datetime import datetime

# 🔧 Scraping logic
def scrape(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {
            "url": url,
            "status": response.status_code,
            "content_length": len(response.text)
        }
    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }

# 📝 Generate urls.txt with properly formatted URLs
def generate_urls():
    urls = [
    "https://www.newegg.com/hp-prodesk-400-g5-nettop-computer/p/N82E16883997492",
    "https://www.newegg.com/p/N82E16834360261",
    "https://www.newegg.com/p/N82E16834233251",
    "https://www.newegg.com/p/N82E16834360335",
    "https://www.newegg.com/p/N82E16834233252"
]
    with open("urls.txt", "w") as f:
        f.write("\n".join(urls))

# 🚀 Main workflow
def main():
    generate_urls()

    with open("urls.txt") as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []
    for url in urls:
        results.append(scrape(url))

    df = pd.DataFrame(results)

    today = datetime.utcnow().strftime("%Y-%m-%d")
    output_filename = f"output_{today}.csv"
    df.to_csv(output_filename, index=False)
    print(f"✅ Saved results to {output_filename}")

# 🏁 Entry point
if __name__ == "__main__":
    main()


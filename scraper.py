import requests
import pandas as pd
from datetime import datetime

# 🔧 Replace this with your actual scraping logic
def scrape(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Example: return page title or status code
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

# 📝 Generate urls.txt dynamically
def generate_urls():
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
    with open("urls.txt", "w") as f:
        f.write("\n".join(urls))

# 🚀 Main workflow
def main():
    generate_urls()  # ✅ Create urls.txt

    with open("urls.txt") as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []
    for url in urls:
        result = scrape(url)
        results.append(result)

    df = pd.DataFrame(results)

    # Save to dated CSV
    today = datetime.utcnow().strftime("%Y-%m-%d")
    output_filename = f"output_{today}.csv"
    df.to_csv(output_filename, index=False)
    print(f"✅ Saved results to {output_filename}")

# 🏁 Entry point
if __name__ == "__main__":
    main()


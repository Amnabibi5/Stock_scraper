import requests
import pandas as pd
from datetime import datetime
import os

def scrape(url):
    """Scrape a single URL and return results"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return {
            "url": url,
            "status": response.status_code,
            "content_length": len(response.text),
            "timestamp": datetime.utcnow().isoformat()
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

def get_urls():
    """Return list of URLs to scrape"""
    return [
        "https://example.com",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://httpbin.org/json"
    ]

def main():
    """Main scraping workflow"""
    print("🚀 Starting web scraper...")
    
    # Get URLs to scrape
    urls = get_urls()
    print(f"📋 Found {len(urls)} URLs to scrape")
    
    # Scrape each URL
    results = []
    for i, url in enumerate(urls, 1):
        print(f"🔍 Scraping {i}/{len(urls)}: {url}")
        result = scrape(url)
        results.append(result)
    
    # Create DataFrame and save results
    df = pd.DataFrame(results)
    
    # Use GitHub workspace directory if available, otherwise current directory
    workspace = os.getenv('GITHUB_WORKSPACE', '.')
    today = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = os.path.join(workspace, f"scrape_results_{today}.csv")
    
    # Save to CSV
    df.to_csv(output_filename, index=False)
    print(f"✅ Results saved to {output_filename}")
    
    # Print summary
    successful_scrapes = len(df[df['status'] != 'error'])
    failed_scrapes = len(df[df['status'] == 'error'])
    print(f"📊 Summary: {successful_scrapes} successful, {failed_scrapes} failed")
    
    return df

if __name__ == "__main__":
    main()

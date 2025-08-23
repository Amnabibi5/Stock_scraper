import requests
import pandas as pd
from datetime import datetime
import os

def scrape(url):
    """Scrape a single URL and return results"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Extract more useful data
        content = response.text
        return {
            "url": url,
            "status": response.status_code,
            "content_length": len(content),
            "response_time": response.elapsed.total_seconds(),
            "contains_stock_data": "stock" in content.lower() or "price" in content.lower(),
            "title": extract_title(content),
            "timestamp": datetime.utcnow().isoformat()
        }
    except requests.exceptions.RequestException as e:
        return {
            "url": url,
            "status": "error",
            "error": str(e),
            "response_time": 0,
            "contains_stock_data": False,
            "title": "",
            "timestamp": datetime.utcnow().isoformat()
        }

def extract_title(html_content):
    """Extract page title from HTML content"""
    try:
        import re
        match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if match:
            return match.group(1).strip()[:100]  # Limit to 100 chars
    except:
        pass
    return ""

def get_urls():
    """Return list of URLs to scrape from urls.txt file"""
    urls = []
    
    try:
        # Try to read from urls.txt file
        with open('urls.txt', 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments (lines starting with #)
                if not line or line.startswith('#'):
                    continue
                
                # Basic URL validation
                if line.startswith(('http://', 'https://')):
                    urls.append(line)
                    print(f"✓ Loaded URL {len(urls)}: {line}")
                else:
                    print(f"⚠ Warning: Invalid URL on line {line_num}: {line}")
        
        if urls:
            print(f"📋 Successfully loaded {len(urls)} URLs from urls.txt")
            return urls
        else:
            print("⚠ No valid URLs found in urls.txt")
            
    except FileNotFoundError:
        print("❌ urls.txt file not found! Using fallback URLs.")
    except Exception as e:
        print(f"❌ Error reading urls.txt: {e}")
    
    # Fallback URLs if file reading fails
    print("🔄 Using fallback test URLs")
    return [
        "https://httpbin.org/status/200",
        "https://httpbin.org/json",
        "https://example.com"
    ]

def main():
    """Main scraping workflow"""
    print("Starting web scraper...")
    
    urls = get_urls()
    print(f"Found {len(urls)} URLs to scrape")
    
    results = []
    for i, url in enumerate(urls, 1):
        print(f"Scraping {i}/{len(urls)}: {url}")
        result = scrape(url)
        results.append(result)
    
    df = pd.DataFrame(results)
    
    workspace = os.getenv('GITHUB_WORKSPACE', '.')
    today = datetime.utcnow().strftime("%Y-%m-%d")
    output_filename = os.path.join(workspace, f"output_{today}.csv")
    
    df.to_csv(output_filename, index=False)
    print(f"Results saved to {output_filename}")
    
    successful_scrapes = len(df[df['status'] != 'error'])
    failed_scrapes = len(df[df['status'] == 'error'])
    print(f"Summary: {successful_scrapes} successful, {failed_scrapes} failed")
    
    return df

if __name__ == "__main__":
    main()

# 🛒 Daily Stock Status Scraper

This project automates the daily scraping of stock availability from a list of product URLs. It runs via GitHub Actions every morning and logs results to `output.csv`.

## 🔧 Features
- Scrapes static product pages using `requests` + `BeautifulSoup`
- Logs stock status with timestamp
- Automated daily run via GitHub Actions
- Modular, reproducible, and easy to extend

## 📁 File Structure

├── scraper.py # Main script
 ├── urls.txt # List of product URLs
  ├── output.csv # Daily results 
  ├── requirements.txt # Python dependencies 
  └── .github/workflows/ 
  └── daily_scrape.yml # GitHub Actions workflow

  
## 🚀 How It Works
1. Reads URLs from `urls.txt`
2. Scrapes stock status using a CSS selector
3. Saves results to `output.csv`
4. Commits results daily via GitHub Actions

## 📅 Automation
Runs daily at 10 AM PKT (5 AM UTC). You can also trigger it manually from the Actions tab.

## 📦 Dependencies
```bash
pip install -r requirements.txt

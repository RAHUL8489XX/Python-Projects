import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import time

class WebScraperAnalyzer:
    def __init__(self, url):
        self.url = url
        self.data = []
        
    def scrape_links(self):
        """Scrape all links from the given URL"""
        response = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            text = link.get_text(strip=True)
            self.data.append({
                'text': text,
                'href': href,
                'length': len(text)
            })
        return pd.DataFrame(self.data)
    
    def analyze_data(self, df):
        """Perform analysis on scraped link data"""
        print("\n=== DATA ANALYSIS ===")
        print(f"Total links scraped: {len(df)}")
        print(f"\nTop 5 Link Texts:")
        print(df['text'].value_counts().head())
        print(f"\nTop 5 Link URLs:")
        print(df['href'].value_counts().head())
        print(f"\nAverage link text length: {df['length'].mean():.2f} characters")
        return Counter(df['text'])
    
    def visualize(self, text_counts):
        """Create visualizations for link text frequency"""
        top_texts = dict(text_counts.most_common(10))
        plt.figure(figsize=(10, 6))
        plt.bar(top_texts.keys(), top_texts.values(), color='skyblue')
        plt.xlabel('Link Text')
        plt.ylabel('Frequency')
        plt.title('Top 10 Most Common Link Texts')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('link_text_analysis.png')
        print("\nVisualization saved as 'link_text_analysis.png'")

# Usage Example
if __name__ == "__main__":
    # Create scraper instance for any URL
    url = input("Enter the URL to scrape: ")
    scraper = WebScraperAnalyzer(url)
    print("Starting web scraping...")
    df = scraper.scrape_links()
    text_counts = scraper.analyze_data(df)
    scraper.visualize(text_counts)
    df.to_csv('scraped_links.csv', index=False)
    print("\nData saved to 'scraped_links.csv'")
    print("\nDone! Check the files for results.")
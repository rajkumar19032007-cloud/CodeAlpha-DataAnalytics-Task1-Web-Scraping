import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

def scrape_books(pages=3):
    """
    Scrapes book data from books.toscrape.com
    Handles HTML + pagination + errors
    """
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    books_data = []

    print(f"Starting scrape at {datetime.now()}")

    for page in range(1, pages + 1):
        url = base_url.format(page)
        print(f"Scraping page {page}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            books = soup.find_all('article', class_='product_pod')

            for book in books:
                title = book.h3.a['title']
                price = book.find('p', class_='price_color').text.replace('£', '')
                rating = book.find('p', class_='star-rating')['class'][1]
                availability = book.find('p', class_='instock').text.strip()

                books_data.append({
                    'Title': title,
                    'Price_GBP': float(price),
                    'Rating': rating,
                    'In_Stock': 'In stock' in availability,
                    'Scraped_Date': datetime.now().date()
                })

            time.sleep(1) # Respect website

        except Exception as e:
            print(f"Error on page {page}: {e}")
            continue

    print(f"Scraped {len(books_data)} books total")
    return books_data

def create_custom_dataset(data):
    """Save data to CSV"""
    df = pd.DataFrame(data)
    df['Price_GBP'] = pd.to_numeric(df['Price_GBP'], errors='coerce')
    df.to_csv('custom_books_dataset.csv', index=False)
    print(f"Dataset saved! Shape: {df.shape}")
    print(df.head())
    return df

if __name__ == "__main__":
    data = scrape_books(pages=3)
    create_custom_dataset(data)
    print("\n✅ Task 1 Complete")

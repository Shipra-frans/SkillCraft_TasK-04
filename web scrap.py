from bs4 import BeautifulSoup
import requests
import pandas as pd

# Amazon Bestsellers - Beauty
url = "https://www.amazon.in/gp/bestsellers/beauty/1374302031"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.content, "html.parser")

# Find all product containers
items = soup.find_all('div', class_='p13n-sc-uncoverable-faceout')  # or use 'zg-grid-general-faceout'

products = []

for item in items:
    title_tag = item.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
    title = title_tag.get_text(strip=True) if title_tag else "No title"

    link_tag = item.find('a', class_='a-link-normal')
    product_url = f"https://www.amazon.in{link_tag['href']}" if link_tag and 'href' in link_tag.attrs else "No URL"

    price_tag = item.find('span', class_='_cDEzb_p13n-sc-price_3mJ9Z')
    price = price_tag.get_text(strip=True) if price_tag else "No price"

    rating_tag = item.find('span', class_='a-icon-alt')
    rating = rating_tag.get_text(strip=True) if rating_tag else "No rating"

    products.append({
        'Title': title,
        'Price': price,
        'Rating': rating,
        'URL': product_url
    })

# Convert to DataFrame
df = pd.DataFrame(products)
print(df)

# Save to CSV
df.to_csv("amazon_bestsellers.csv", index=False, encoding='utf-8')
print("✅ Data scraped and saved to amazon_bestsellers.csv")
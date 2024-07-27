# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import time
import os, re
from pathlib import Path
import redis
from urllib.parse import urljoin


class Scraper:
    def __init__(self, page_limit=None, proxy=None):
        self.base_url = "https://dentalstall.com/shop/page/{}/"
        self.first_page_url = "https://dentalstall.com/shop"
        self.page_limit = page_limit
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.products = []
        self.products_scraped = 0
        self.cache = redis.Redis(host='localhost', port=6379, db=0)
        self.data_file = Path("products.json")

    def scrape_catalogue(self):
        page = 1
        while True:
            if self.page_limit and page > self.page_limit:
                break

            if page == 1:
                url = self.first_page_url
            else:
                url = self.base_url.format(page)

            response = self.get_response(url)
            if not response:
                break

            soup = BeautifulSoup(response.content, 'html.parser')
            product_elements = soup.find_all('li', class_='product')

            if not product_elements:
                break

            for product in product_elements:
                title = product.find('h2', class_='woo-loop-product__title').text
                price = product.find('span', class_='woocommerce-Price-amount').text.strip()
                price = self.clean_price(price)
                image_full_url = product.find('img', class_='attachment-woocommerce_thumbnail')['data-lazy-src']
                image_path = self.download_image(image_full_url, title)
                product_data = {
                    "product_title": title,
                    "product_price": f"₹{price}",
                    "path_to_image": image_path
                }

                cache_key = f"product:{title}"
                cached_price = self.cache.get(cache_key)
                if cached_price and cached_price.decode('utf-8') == price:
                    continue

                self.cache.set(cache_key, price, ex=300)
                self.products.append(product_data)
                self.products_scraped += 1

            page += 1

        self.save_to_file()
        print(f"Scraped {self.products_scraped} products.")

    def get_response(self, url):
        for _ in range(3):
            try:
                response = requests.get(url, proxies=self.proxy, timeout=10)
                if response.status_code == 200:
                    return response
            except requests.RequestException:
                time.sleep(5)
        return None

    def download_image(self, url, title):
        image_response = requests.get(url, stream=True)
        print("image_response", image_response)
        if image_response.status_code == 200:
            image_path = Path(f"images/{title}.jpg")
            image_path.parent.mkdir(parents=True, exist_ok=True)
            with open(image_path, 'wb') as file:
                for chunk in image_response.iter_content(1024):
                    file.write(chunk)
            return str(image_path)
        return ""

    def clean_price(self, price):
        return re.sub(r'[^\d.]', '', price)


    def save_to_file(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.products, file, ensure_ascii=False)

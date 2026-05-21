# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from typing import Optional
import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

def price_serializer(value: str) -> Optional[float]:
    if not value:
        return None
    numeric = re.sub(r'[^\d.]', '', value.strip())
    try:
        return float(numeric)
    except ValueError:
        return None

def convert_stars_to_int(star_string):
    """Convert a star rating string (e.g., 'star-rating One') to an integer 1-5."""
    word_to_int = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5
    }
    
    # Normalize: lowercase, remove extra whitespace, split into words
    words = star_string.lower().strip().split()
    
    for word in words:
        # Strip common punctuation that might trail the word (e.g., "Five." or "One!")
        clean_word = word.strip(".,;:!?")
        if clean_word in word_to_int:
            return word_to_int[clean_word]
            
    # Fallback: handle cases where the rating is already numeric (e.g., "star-rating 3")
    for word in words:
        if word.isdigit():
            num = int(word)
            if 1 <= num <= 5:
                return num
                
    raise 0

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Remove all whitespaces
        field_names = adapter.field_names()

        price_field_names =['price_excl_tax', 'price_incl_tax', 'tax', 'price']
        types_name = ['product_type', 'category']
        for field_name in field_names:
            if field_name in price_field_names:
                value = adapter.get(field_name)
                adapter[field_name] = price_serializer(value)
            elif field_name in types_name:
                value = adapter.get(field_name)
                adapter[field_name] = value.lower()
            elif field_name.lower() == 'availability':
                availability_string = adapter.get('availability')
                split_string_array = availability_string.split('(')
                if len(split_string_array) < 2:
                    adapter[field_name] = 0
                else:
                    availability_array = split_string_array[1].split(' ')
                    adapter[field_name] = int(availability_array[0])
            elif field_name.lower() == 'num_reviews':
                num_reviews_string = adapter.get('num_reviews')
                adapter[field_name] = int(num_reviews_string)
            elif field_name.lower() == 'stars':
                stars_num_string = adapter.get('stars')
                adapter[field_name] = convert_stars_to_int(stars_num_string)
            else:
                value = adapter.get(field_name)
                adapter[field_name] = value.strip() if value is not None else ''
        return item

import mysql.connector

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 123,
            database = 'scrapebooks'
        )

        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                url VARCHAR(1024) UNIQUE NOT NULL,
                title VARCHAR(255),
                product_type VARCHAR(100),
                price_excl_tax DECIMAL(10, 2),
                price_incl_tax DECIMAL(10, 2),
                tax DECIMAL(10, 2),
                availability VARCHAR(100),
                num_reviews INT,
                stars VARCHAR(50),
                category VARCHAR(100),
                description TEXT,
                price DECIMAL(10, 2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""")
    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO books (url, title, product_type, price_excl_tax, price_incl_tax, tax, availability, num_reviews, stars, category, description, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                title = VALUES(title),
                price = VALUES(price),
                availability = VALUES(availability),
                updated_at = CURRENT_TIMESTAMP;
""")
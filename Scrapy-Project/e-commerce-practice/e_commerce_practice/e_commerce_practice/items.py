# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from dataclasses import dataclass, field
from typing import Optional

from itemloaders.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


@dataclass
class ECommercePracticeItem:
    # define the fields for your item here like:
    # name: str | None = None
    pass

@dataclass
class ProductItem:
    # Product identification
    product_code: Optional[str] = None
    product_name: Optional[str] = None

    # Pricing
    full_price: Optional[float] = None
    price: Optional[float] = None
    currency_code: Optional[str] = None

    # Location
    country_code: Optional[str] = None

    # URLs
    item_url: Optional[str] = None
    image_url: Optional[str] = None

    # Classification
    gender: Optional[str] = None
    product_category: Optional[str] = None
    product_subcategory: Optional[str] = None

def to_float(value):
    if value is None:
        return None
    value = str(value).replace(",", "").replace("$", "").strip()
    return float(value) if value else None


def clean_text(value):
    return value.strip() if value else None


class ProductItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

    # Pricing
    full_price = MapCompose(to_float)
    price = MapCompose(to_float)
    currency_code = MapCompose(str.upper, clean_text)

    # Product identification
    product_name = MapCompose(clean_text)
    product_code = MapCompose(clean_text)

    # Classification
    gender = MapCompose(str.lower, clean_text)
    product_category = MapCompose(str.lower, clean_text)
    product_subcategory = MapCompose(str.lower, clean_text)

    # URLs
    item_url = MapCompose(clean_text)
    image_url = MapCompose(clean_text)
    
    # Location
    country_code = MapCompose(str.upper, clean_text)

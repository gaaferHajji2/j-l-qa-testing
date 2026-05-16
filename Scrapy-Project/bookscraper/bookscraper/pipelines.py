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
            elif field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
            

        return item

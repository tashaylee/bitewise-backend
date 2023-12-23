import json
import os
from django.core.management.base import BaseCommand
from food_product.models import FoodProduct
from django.db import models

class Command(BaseCommand):
    help = 'Seed the database with initial FSIS data'

    def handle(self, *args, **options):
        # references current file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.abspath(os.path.join(current_dir, '../../../../'))
        json_file_path = os.path.join(backend_dir, 'fsis_food_items.json')

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

            # Extract Product data
            sheets = data.get("sheets")
            products_data = sheets[2].get("data")

            for product_item in products_data:
                field_values = {}

                for item_field in product_item:
                    # make field name lowercase
                    key, value = next(iter(item_field.items()))
                    key = key.lower()

                    # Replace None values with a empty string
                    value = value if value is not None else None

                    # add the key and value to  field_values
                    field_values[key] = value

                # create a FoodProduct object with all field values
                food_product = FoodProduct(**field_values)
                food_product.save()
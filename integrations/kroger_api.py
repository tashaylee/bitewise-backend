import os
import base64
import requests
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.cache import cache
from urllib.parse import urlencode

from ingredients.ingredients_service import default as ingredients_service


# TO DO: external caching + async request or batch endpoints
class KrogerAPI:
    def __init__(self) -> None:
        self.__app_id = os.getenv("kroger_client_id")
        self.__app_key = os.getenv("kroger_client_secret")

        self._headers = {
            "Content-Type": "application/json"
        }
        
        self._data = {
            "grant_type": "client_credentials"
        }

    def __base_url(self, type: str):
        api_base_url = 'https://api-ce.kroger.com/v1/'

        endpoints = {
            'products': 'products',
            'locations': 'locations',
            'auth': 'connect/oauth2/token'
        }

        url = f"{api_base_url}{endpoints.get(type, '')}"

        if type == 'auth':
            credentials = f"{self.__app_id}:{self.__app_key}"
            base64_credentials = base64.b64encode(credentials.encode()).decode("utf-8")
            self._headers["Content-Type"] = "application/x-www-form-urlencoded"
            self._headers['Authorization'] = f"Basic {base64_credentials}"
            self._data["scope"] = 'product.compact'

        return url

    def _set_token(self):
       # checks if kroger bearer tokens are in cache
        access_token = cache.get('kroger_access_token')
        expires_at = cache.get('kroger_expires_at', 0)

        # checks if tokens are still valid
        if access_token and time.time() < expires_at:
            return

        url = self.__base_url('auth')
        response = requests.post(url, headers=self._headers, data=self._data)
        
        if response.status_code == 200:
            token_response = response.json()
            access_token = token_response.get("access_token")
            expires_in = token_response.get("expires_in")

            # adds token and expiration time to cache
            cache.set('kroger_access_token', access_token, expires_in)
            cache.set('kroger_expires_at', time.time() + expires_in)
            
            # sets headers
            self._headers['Authorization'] = f"Bearer {access_token}"
            self._headers["Content-Type"] = "application/json"
        
        else:
            return response.text
    
    def __filter_location_ids(self, response):
        locations = []
        for location in response.json().get('data', []):
            location_id = location.get('locationId', None)
            location_name = location.get('name', None)
            location_info = {location_id: location_name}
            locations.append(location_info)

        return locations
    
    def fetch_locations(self, lat, long):
        self._set_token()
        url = self.__base_url('locations')
        params = {
            'filter.latLong.near': f"{lat},{long}"
        }

        try:
            response = requests.get(url, headers=self._headers, params=params)

            if response.status_code == 200:
                return self.__filter_location_ids(response)
            return response
        except Exception as e:
            return e

    # TO DO: consider when store_id doesnt carry items needed for recipe
    def fetch_prices(self, store_id, shopping_list):
        self._set_token()
        url = self.__base_url('products')

        params = {
            'filter.locationId': store_id,
            'filter.limit': 10,
        }

        item_prices = []

        for recipe in shopping_list:
            ingredients = recipe.get('ingredients', [])
            ingredient_names = ingredients_service.extract_ingredients(ingredients)
            price_dict = self.__fetch_recipe_prices(url, params, recipe, ingredient_names)
            item_prices.append(price_dict)

        return item_prices

    def __fetch_recipe_prices(self, url, params, recipe, ingredient_names):
        price_dict = {
            'recipe_label': recipe.get('recipeLabel'),
            'ingredient_prices': [],
        }
        with ThreadPoolExecutor() as executor:
            # Submit tasks for each ingredient
            futures = [executor.submit(self.__fetch_ingredient_data, url, params, ingredient) for ingredient in ingredient_names]

            # Wait for all tasks to complete
            for future in as_completed(futures):
                ingredient_data = future.result()
                if ingredient_data.values():
                    price_dict['ingredient_prices'].append(ingredient_data)

        return price_dict

    def __fetch_ingredient_data(self, url, params, ingredient):
        ingredient_data = {}
        params['filter.term'] = ingredient

        try:
            response = requests.get(url, headers=self._headers, params=urlencode(params))

            if response.status_code == 200:
                items_data = response.json().get('data', [])
                for query_item in items_data:
                    description = query_item.get('description', None)
                    items = query_item.get('items', None)

                    if description and items:
                        self.__process_items_data(ingredient_data, description, items)

        except Exception as e:
            return e

        return ingredient_data

    def __process_items_data(self, ingredient_data, description, items):
        for item in items:
            price = item.get('price', None)
            if price:
                current_item_price = ingredients_service.get_promo_price(price)
                self.__update_ingredient_data(ingredient_data, description, current_item_price)


    def __update_ingredient_data(self, ingredient_data, description, current_item_price):
        if not ingredient_data:
            ingredient_data.update({'description': description, 'price': current_item_price})
        elif ingredient_data['price'] is not None and current_item_price < ingredient_data['price']:
            ingredient_data.update({'description': description, 'price': current_item_price})

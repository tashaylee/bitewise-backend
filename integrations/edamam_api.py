from dotenv import load_dotenv; load_dotenv()
import os
import requests

class EdamamAPI:
    def __init__(self) -> None:
        self.base = 'https://api.edamam.com/api/recipes/v2?'
        self.app_id = os.getenv("edamam_app_id")
        self.app_key = os.getenv("edamam_app_key")
    
    def __base_url(self):
        return f'{self.base}&app_id={self.app_id}&app_key={self.app_key}&type=public&'

    def get_recipes(self, search_term, max_ingr, max_time):
        recipe_info = []
        url = f'{self.__base_url()}q={search_term}&time={max_time}&ingr={max_ingr}'
        response = requests.get(url)
        hits = response.json().get('hits')
        
        for item in hits:
            recipe = item.get('recipe', None)
            recipe_label = recipe.get('label', None)
            recipe_url = recipe.get('url', None)
            ingredients = recipe.get('ingredientLines', None)

            recipe_data = {'recipe_label': recipe_label, 'recipe_url': recipe_url, 'ingredients': str(ingredients)}
            recipe_info.append(recipe_data)
        return recipe_info
        
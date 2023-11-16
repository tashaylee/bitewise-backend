import pytest
from unittest.mock import patch
from rest_framework.response import Response
import json


recipe_data = {
    'search_term': 'chicken wings',
    'max_time': '45',
    'max_ingr': '8',
}

location_data = {
    'latitude':'39.306346',
    'longitude': '-84.278902',
}

shopping_list_data = {'shoppingList': [{'recipeLabel': 'Five-Spice Chicken Wings', \
                                        'ingredients': ['1 1/2 teaspoons minced garlic', '1 1/2 teaspoons Chinese five-spice powder', '1 1/4 teaspoons salt', '1 1/2 teaspoons soy sauce', '3 lb chicken wings (about 16)']}, \
                                        {'recipeLabel': 'Lime & Chilli Chicken Wings', \
                                        'ingredients': ['2 limes , zested and juiced', '1.0kg chicken wings or thighs', '4 red chillies and green chillies, seeded and finely chopped', '3.0 tbsp sugar', 'sweet chilli sauce , to serve']}],
                        'store_id': '01400376'}

@pytest.mark.django_db
class TestIntegration:
    def test_get_recipes(self, auth_client):
        expected_response_data = [{'recipe_label': 'Ginger Honey Chicken Wings recipes', 'recipe_url': 'http://www.simplyrecipes.com/recipes/ginger_honey_chicken_wings/', 'ingredients': "['3 pounds chicken wing drummettes', '1 green onion, thinly sliced on the diagonal', '2 Tbsp toasted sesame seeds', '1/4 cup soy sauce (use gluten-free soy sauce if cooking gluten-free)', '3 Tbsp honey', '1-inch piece of ginger, peeled and grated', '3 cloves garlic, finely minced', '1/8 teaspoon sriracha hot sauce (or other hot sauce)']"}, {'recipe_label': 'Herb Grilled Chicken Wings', 'recipe_url': 'https://www.epicurious.com/recipes/food/views/herb-grilled-chicken-wings-51175360', 'ingredients': "['4 garlic cloves, finely chopped', '1/4 cup chopped fresh oregano', '1/4 cup chopped fresh rosemary', '1/4 cup olive oil', 'Kosher salt, freshly ground pepper', '2 pounds chicken wings']"}, {'recipe_label': 'When Pigs Fly Wings Recipe', 'recipe_url': 'http://www.foodrepublic.com/2011/09/07/when-pigs-fly-wings-recipe', 'ingredients': "['3 cups pork rinds', '2 large eggs', '4 tablespoons butter, melted and slightly cooled', '12 chicken wings, cut in half at joints, wing tips removed and discarded']"}, {'recipe_label': 'Honey Ginger Chicken Wings', 'recipe_url': 'https://food52.com/recipes/30411-honey-ginger-chicken-wings', 'ingredients': "['16 pieces Free-range chicken wings or just drumsticks (my preference)', '¼ cups honey', '2 tablespoons gluten free tamari sauce', '2 tablespoons freshy grated ginger', '1 tablespoon freshly squeezed lime juice', '2 pieces garlic cloves, minced', '1/2 teaspoon freshly ground black pepper']"}]
        mock_response = Response(expected_response_data)

        with patch('integrations.views.EdamamAPIView.get', return_value=mock_response):
            response = auth_client.get('/api/recipes/', data=recipe_data)
            assert response.status_code == 200
            assert len(response.data) == 4

            labels = ['recipe_label', 'recipe_url', 'ingredients']
            for label in labels:
                assert label in response.data[0].keys()
    
    def test_get_locations(self, api_client):
        expected_response_data = [{'01400376': 'Kroger - Landen'}, {'01400053': 'Kroger Fuel - Harpers Point Fuel'}, {'01400448': 'Kroger - Mason Montgomery Mason OH'}, {'01400413': 'Kroger - Loveland'}, {'01400353': 'Kroger - Harpers Point'}, {'01400426': 'Kroger - Kings Mills Mason'}, {'01400408': 'Kroger - Maineville'}, {'014LS994': 'Lab Location Blue As - Lab Location Blue As'}, {'701LS993': 'FRED MEYER STORES - FRED MEYER STORES'}]
        mock_response = Response(expected_response_data)

        with patch('integrations.views.LocationsAPIView.get', return_value=mock_response):
            response = api_client.get('/api/locations/', data=location_data)
            assert response.status_code == 200

    def test_post_shopping_list(self, api_client):
        expected_response_data = [{'recipe_label': 'Five-Spice Chicken Wings', 'ingredient_prices': [{'description': 'Spice World Minced Garlic', 'price': 1.99}, {'description': 'Chinese Five Spice Seasoning Powder', 'price': 4.99}, {'description': 'Kroger Iodized Salt', 'price': 0.59}, {'description': 'Kikkoman Soy Sauce', 'price': 2.99}, {'description': 'Kroger Chicken Wings', 'price': 5.99}]}]
        mock_response = Response(expected_response_data)
        with patch('integrations.views.ShoppingListAPIView.post', return_value=mock_response):

            response = api_client.post('/api/shopping-lists/', data=json.dumps(shopping_list_data), content_type='application/json')
            data= response.data
            assert response.status_code == 200
            assert len(data) == 1
            
            for data_response in data:
                assert 'recipe_label' in data_response.keys() and 'ingredient_prices' in data_response.keys()
                assert len(data_response['ingredient_prices'])> 0
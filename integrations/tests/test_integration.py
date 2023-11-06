import pytest
from unittest.mock import patch
from rest_framework.response import Response


recipe_data = {
    'search_term': 'chicken wings',
    'max_time': '45',
    'max_ingr': '8',
}

@pytest.mark.django_db
class TestIntegration:
    def test_get_integration(self, auth_client):
        expected_response_data = [{'recipe_label': 'Baked Chicken Wings', 'recipe_url': 'https://www.marthastewart.com/1140985/baked-chicken-wings', 'ingredients': "['3 pounds chicken wings, cut in half at joints, wing tips removed', 'Coarse salt']"}, {'recipe_label': 'Five-Spice Chicken Wings', 'recipe_url': 'https://www.epicurious.com/recipes/food/views/five-spice-chicken-wings-109520', 'ingredients': "['1 1/2 teaspoons minced garlic', '1 1/2 teaspoons Chinese five-spice powder', '1 1/4 teaspoons salt', '1 1/2 teaspoons soy sauce', '3 lb chicken wings (about 16)']"}, {'recipe_label': 'Lime & Chilli Chicken Wings', 'recipe_url': 'http://www.bbcgoodfood.com/recipes/3717/', 'ingredients': "['2 limes , zested and juiced', '1.0kg chicken wings or thighs', '4 red chillies and green chillies, seeded and finely chopped', '3.0 tbsp sugar', 'sweet chilli sauce , to serve']"}, {'recipe_label': 'Coconut Cilantro Chicken Wings', 'recipe_url': 'https://food52.com/recipes/26598-coconut-cilantro-chicken-wings', 'ingredients': "['12 chicken wings', '1 teaspoon garlic powder', '1 teaspoon ground cumin', '1/4 cup honey', '1/8 cup coconut cream', '1/2 cup unsweetened coconut shreds', '3 tablespoons chopped fresh cilantro, to serve']"}, {'recipe_label': 'Coriander And Lime Chicken Wings', 'recipe_url': 'http://www.saveur.com/article/Recipes/Coriander-and-Lime-Chicken-Wings', 'ingredients': "['2 lbs. chicken wings, separated into 2 pieces', '3 tbsp. fresh lime juice', '1 tbsp. cracked coriander seeds', '½ tsp. crushed red chile flakes', '3 cloves garlic, minced', 'Kosher salt, to taste', 'Nuoc cham, for serving']"}, {'recipe_label': 'Coca-Cola–Glazed Chicken Wings', 'recipe_url': 'http://imbibemagazine.com/Coca-Cola%E2%80%93Glazed-Chicken-Wings-Recipe', 'ingredients': "['1 cup Coca-Cola Classic', 'Juice of 2 limes', '1 1/2 cups firmly packed light brown sugar', '3 jalapeño chiles, finely chopped, plus 2 jalapeño chiles, sliced, for garnish', '3 lbs. chicken wings (12–14 whole wings)', 'Coarse salt and freshly ground black pepper']"}, {'recipe_label': 'Apricot Chicken Wings', 'recipe_url': 'http://www.thedailymeal.com/apricot-chicken-wings-recipe', 'ingredients': "['2 Pounds chicken wings', '1 Cup apricot preserves', '2 Tablespoons apple cider vinegar', '2 Teaspoons hot pepper sauce', '1 Teaspoon chile powder', '1 clove garlic, minced']"}, {'recipe_label': 'Perfect, Uncluttered Chicken Stock', 'recipe_url': 'http://smittenkitchen.com/blog/2013/11/perfect-uncluttered-chicken-stock/', 'ingredients': "['3 pounds uncooked chicken wings', '3 quarts water', '1 large onion, chopped', '1 garlic clove, smashed', '1 teaspoon table salt, or more to taste*']"}, {'recipe_label': "Red Onion's Glazed Chicken Wings", 'recipe_url': 'http://www.latimes.com/features/food/la-fo-glazed-chicken-wings-s,0,2048139.story', 'ingredients': "['2 cups rice wine vinegar', '2 cups light brown sugar, packed', '1/2 cup granulated sugar', '1/4 cup chili sauce', '1 1/2 tablespoons hot pepper sauce', '1 1/2 tablespoons liquid smoke', '2 dozen chicken wings, or more']"}, {'recipe_label': 'Baked Chicken Wings', 'recipe_url': 'https://www.delish.com/cooking/recipe-ideas/recipes/a53411/easy-oven-baked-chicken-wings/', 'ingredients': "['3 lb. chicken wings, split at the joint, wing tips removed and discarded', '4 tbsp. vegetable oil', 'kosher salt', 'Freshly ground black pepper', '3/4 tsp. garlic powder', '3 tsp. baking powder']"}, {'recipe_label': 'Maple Chicken Wings', 'recipe_url': 'http://www.myrecipes.com/recipe/maple-chicken-wings', 'ingredients': "['2 to 3 pounds chicken wings', '1 cup maple syrup', '2/3 cup chili sauce', '1/2 cup onion, finely chopped', '2 tablespoons Dijon mustard', '2 tablespoons Worcestershire sauce', '1/4 to 1/2 teaspoon red pepper flakes']"}, {'recipe_label': 'Super Bowl Snacks: Slow-Fried Buffalo Wings Recipe', 'recipe_url': 'http://www.seriouseats.com/recipes/2009/01/slow-fried-momofuku-inspired-buffalo-chicken-wings-recipe.html', 'ingredients': '[\'10 chicken wings\', \'2 1/2 cups pork fat, duck fat, or beef fat\', \'2 tablespoons butter\', \'1/2 tablespoon brown sugar\', "3 tablespoons Frank\'s Hot Sauce", \'1 teaspoon cider vinegar\', \'1 tablespoon Tabasco Sauce\']'}, {'recipe_label': "Maria's Hot Buffalo Chicken Wings", 'recipe_url': 'https://www.menshealth.com/recipes/marias-hot-buffalo-chicken-wings', 'ingredients': '[\'24 organic chicken wings--frozen or fresh\', \'4 tablespoons organic butter\', "1 cup franks\'s original hot sauce. (I\'m sorry, but this is the only choice!)"]'}, {'recipe_label': 'Broiled Chicken Wings with Spicy Peach Glaze recipes', 'recipe_url': 'http://www.foodandwine.com/blogs/2014/6/26/how-to-make-incredible-chicken-wings-without-a-grill?xid=blog_20140629_26855396', 'ingredients': "['12 oz. peach preserves', '2 Tbsp. cider vinegar', '1 tsp. soy sauce', '2 tsp. Sriracha (or to taste)', '½ tsp. red pepper flakes (or to taste)', '2 Tbsp. butter', '2½ to 3 lbs. chicken wings, tips removed', 'salt']"}, {'recipe_label': 'Campfire Chicken Wings', 'recipe_url': 'https://www.foodnetwork.com/recipes/campfire-chicken-wings-3743993', 'ingredients': '[\'2 pounds chicken wings\', \'1/4 cup olive oil\', \'2 tablespoons lime juice, plus 1 lime cut into wedges\', "One 1.06-ounce packet mesquite grill seasoning mix, such as McCormick\'s Grill Mates Mesquite Marinade", \'2 tablespoons thinly sliced scallions\', \'1 tablespoon fresh cilantro leaves\']'}, {'recipe_label': 'Saffron-Roasted Chicken Wings', 'recipe_url': 'https://www.marthastewart.com/1048762/saffron-roasted-chicken-wings', 'ingredients': "['2 tablespoons extra-virgin olive oil', '2 tablespoons unsalted butter', 'Juice of 1 lemon', '1/4 teaspoon saffron', '6 whole chicken wings', 'Coarse salt and freshly ground black pepper']"}, {'recipe_label': 'Ginger Honey Chicken Wings recipes', 'recipe_url': 'http://www.simplyrecipes.com/recipes/ginger_honey_chicken_wings/', 'ingredients': "['3 pounds chicken wing drummettes', '1 green onion, thinly sliced on the diagonal', '2 Tbsp toasted sesame seeds', '1/4 cup soy sauce (use gluten-free soy sauce if cooking gluten-free)', '3 Tbsp honey', '1-inch piece of ginger, peeled and grated', '3 cloves garlic, finely minced', '1/8 teaspoon sriracha hot sauce (or other hot sauce)']"}, {'recipe_label': 'Herb Grilled Chicken Wings', 'recipe_url': 'https://www.epicurious.com/recipes/food/views/herb-grilled-chicken-wings-51175360', 'ingredients': "['4 garlic cloves, finely chopped', '1/4 cup chopped fresh oregano', '1/4 cup chopped fresh rosemary', '1/4 cup olive oil', 'Kosher salt, freshly ground pepper', '2 pounds chicken wings']"}, {'recipe_label': 'When Pigs Fly Wings Recipe', 'recipe_url': 'http://www.foodrepublic.com/2011/09/07/when-pigs-fly-wings-recipe', 'ingredients': "['3 cups pork rinds', '2 large eggs', '4 tablespoons butter, melted and slightly cooled', '12 chicken wings, cut in half at joints, wing tips removed and discarded']"}, {'recipe_label': 'Honey Ginger Chicken Wings', 'recipe_url': 'https://food52.com/recipes/30411-honey-ginger-chicken-wings', 'ingredients': "['16 pieces Free-range chicken wings or just drumsticks (my preference)', '¼ cups honey', '2 tablespoons gluten free tamari sauce', '2 tablespoons freshy grated ginger', '1 tablespoon freshly squeezed lime juice', '2 pieces garlic cloves, minced', '1/2 teaspoon freshly ground black pepper']"}]
        mock_response = Response(expected_response_data)

        with patch('integrations.views.EdamamAPIView.get', return_value=mock_response):
            response = auth_client.get('/api/recipes/', data=recipe_data)
            assert response.status_code == 200
            assert len(response.data) == 20

            labels = ['recipe_label', 'recipe_url', 'ingredients']
            for label in labels:
                assert label in response.data[0].keys()
from rest_framework.response import Response
from integrations.edamam_api import EdamamAPI
from integrations.kroger_api import KrogerAPI
from rest_framework.views import APIView
import time

class EdamamAPIView(APIView):
    edamam_api = EdamamAPI()

    def get(self, request):
        search_term = request.query_params.get('search_term', None)
        max_ingr = request.query_params.get('max_ingr', None)
        max_time = request.query_params.get('max_time', None)
        
        try:
            response = self.edamam_api.get_recipes(max_ingr=max_ingr, max_time=max_time, search_term=search_term)
            return Response(data=response)
        except Exception as e:
            return Response(data={'error': str(e)})

class LocationsAPIView(APIView):
    kroger_api = KrogerAPI()

    def get(self, request):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)

        try:
            response = self.kroger_api.fetch_locations(lat=latitude, long=longitude)
            return Response(data=response)
        except Exception as e:
            return Response(data={'error': str(e)})
        

class ShoppingListAPIView(APIView):
    kroger_api = KrogerAPI()

    def post(self, request):
        shopping_list = request.data.get('shoppingList', None)
        store_id = request.data.get('store_id', None)
        
        try:
            response = self.kroger_api.fetch_prices(shopping_list= shopping_list, store_id=store_id)
            return Response(data=response, status=200)
        except Exception as e:
            return Response(data={'error': str(e)})
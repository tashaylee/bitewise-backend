from rest_framework.response import Response
from integrations.edamam_api import EdamamAPI
from integrations.kroger_api import KrogerAPI
from rest_framework import viewsets
from rest_framework import status

class EdamamAPIView(viewsets.ModelViewSet):
    edamam_api = EdamamAPI()

    def list(self, request, *args, **kwargs):
        search_term = request.query_params.get('search_term', None)
        max_ingr = request.query_params.get('max_ingr') or '1%2b'
        max_time = request.query_params.get('max_time') or '1%2b'
        
        try:
            response = self.edamam_api.get_recipes(max_ingr=max_ingr, max_time=max_time, search_term=search_term)
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)})

class LocationsAPIView(viewsets.ModelViewSet):
    kroger_api = KrogerAPI()

    def list(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)

        try:
            response = self.kroger_api.fetch_locations(lat=latitude, long=longitude)
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)})
        

class ShoppingListAPIView(viewsets.ModelViewSet):
    kroger_api = KrogerAPI()

    def create(self, request):
        shopping_list = request.data.get('shoppingList', None)
        store_id = request.data.get('store_id', None)
        
        try:
            response = self.kroger_api.fetch_prices(shopping_list= shopping_list, store_id=store_id)
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)})
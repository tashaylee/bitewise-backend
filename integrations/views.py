from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from integrations.edamam_api import EdamamAPI

class EdamamAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    edamam_api = EdamamAPI()

    def get(self, request):
        search_term = request.query_params.get('search_term', None)
        max_ingr = request.query_params.get('max_ingr', None)
        max_time = request.query_params.get('max_time', None)
        
        try:
            response = self.edamam_api.get_recipes(max_ingr=max_ingr, max_time=max_time, search_term=search_term)
        except Exception as e:
            response = e
        return Response(data = response)
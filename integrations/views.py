from rest_framework.response import Response
from integrations.edamam_api import EdamamAPI
from rest_framework.views import APIView

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
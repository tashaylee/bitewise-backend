from rest_framework import viewsets
from .serializers import *
from .models import *

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
class BudgetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_queryset(self):
        user = self.request.user
        return Budget.objects.filter(user=user)
    
    def post(self, request):
        try:
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CommitmentCountView(viewsets.ModelViewSet):
    serializer_class = CommitmentCountSerializer
    queryset = CommitmentCount.objects.all()

class HomeView(APIView):
    permission_classes = (IsAuthenticated, )
    def get(self, request):
        content = {'message': 'Authorized User verified.'}
        return Response(content)

class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
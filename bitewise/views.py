from rest_framework import viewsets
from .serializers import *
from .models import *
from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
class BudgetView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = BudgetSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Budget.objects.filter(user__id=user_id)

    def create(self, request):
        serializer = BudgetSerializer(data=request.data)
        user = request.user
        
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'budget_id' : {serializer.instance.id}}, status=200)
        return Response(serializer.errors,status=400)
    


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CommitmentCountView(viewsets.ModelViewSet):
    serializer_class = CommitmentCountSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        now = datetime.now()
        commitment_counts = CommitmentCount.objects.filter(
            user=user, created_at__year=now.year, created_at__month=now.month, created_at__week=now.isocalendar().week).order_by('-created_at')
        return commitment_counts

    def create(self, request):
        serializer = CommitmentCountSerializer(data=request.data)
        user = request.user
        
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({'commitment_count_id' : {serializer.instance.id}}, status=200)
        return Response(serializer.errors,status=400)


class MealCommitmentView(viewsets.ModelViewSet):
    serializer_class = MealCommitmentSerializer
    queryset = MealCommitment.objects.all()
    permission_classes = [IsAuthenticated,]

    # def get_queryset(self):
    #     user = self.request.user
    #     now = datetime.now()
    #     commitment_count = CommitmentCount.objects.filter(
    #         user=user, created_at__year=now.year, created_at__month=now.month, created_at__week=now.isocalendar().week)
    #     all_commitments = MealCommitment.objects.filter(commitment_count=commitment_count)
    #     return all_commitments


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
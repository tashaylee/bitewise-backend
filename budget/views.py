from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Budget
from .serializers import BudgetSerializer


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
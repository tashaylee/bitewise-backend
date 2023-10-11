from rest_framework import viewsets
from .serializers import *
from .models import *
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
            return Response({'commitment_count_id': {serializer.instance.id}}, status=200)
        return Response(serializer.errors, status=400)


class MealCommitmentView(viewsets.ModelViewSet):
    serializer_class = MealCommitmentSerializer
    queryset = MealCommitment.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        now = datetime.now()
        commitment_count = CommitmentCount.objects.filter(
            user=user, created_at__year=now.year, created_at__month=now.month, created_at__week=now.isocalendar().week)
        all_commitments = MealCommitment.objects.filter(
            commitment_count__in=commitment_count)
        return all_commitments

    def update(self, request, pk=None):
        meal_commitment = get_object_or_404(self.queryset, pk=pk)

        serializer = MealCommitmentSerializer(
            instance=meal_commitment, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'meal_commitment_id': {serializer.instance.id}}, status=200)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'])
    def incomplete(self, request, pk=None):
        qs = self.queryset.filter(
            name=None, cost=0, achieved=None, activated=False)
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=200)

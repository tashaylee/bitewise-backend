from rest_framework import viewsets
from shared.serializers import UserSerializer
from shared.models import User
from rest_framework import viewsets


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
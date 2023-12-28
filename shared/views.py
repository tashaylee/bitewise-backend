from rest_framework import viewsets
from shared.serializers import UserSerializer
from shared.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        user = self.queryset.filter(phone=phone).first()

        if not user:
            user_serializer = UserSerializer(data=request.data)

            if user_serializer.is_valid():
                user= user_serializer.save()
            else:
                return Response({'errors': user_serializer.errors}, status= status.HTTP_406_NOT_ACCEPTABLE)
        
        return Response({'first_name': user.first_name,
                         'last_name': user.last_name,
                         'phone': str(user.phone)}, status=status.HTTP_200_OK)
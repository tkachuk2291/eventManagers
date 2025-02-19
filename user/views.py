from rest_framework import viewsets, status
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer


class UsermodelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            User.objects.create_user(**serializer.validated_data)
        return Response(serializer.data , status=status.HTTP_201_CREATED)



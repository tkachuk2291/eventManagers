from rest_framework import viewsets
from user.models import User
from user.serializers import UserSerializer


class UsermodelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnly]
    queryset = User.objects.all()
    model = User
    serializer_class = UserSerializer
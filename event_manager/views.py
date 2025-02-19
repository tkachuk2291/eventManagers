from rest_framework import viewsets, status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from event_manager.models import Event
from event_manager.serializers import EventSerializer, EventCreateSerializer, EventHandlersSerializer


class EventModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Event.objects.all()
    model = Event
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return EventSerializer
        elif self.action == "create":
            return EventCreateSerializer
        return EventSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)




class EventsHandler(UpdateAPIView , DestroyAPIView  ,  GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventHandlersSerializer

    def put(self , request , *args, **kwargs):
        partial = kwargs.pop('partial', False)
        member_ids = request.data.getlist('members')
        member_ids.append(str(request.user.id))
        new_data = request.data.copy()
        new_data.setlist('members', member_ids)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=new_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "User joined for event"}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.members.filter(id=request.user.id).exists():
            instance.members.remove(request.user)
            instance.save()
            return Response({"message": "User Deleted for event"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)
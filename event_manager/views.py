from rest_framework import viewsets
from event_manager.models import Event
from event_manager.serializers import EventSerializer



class EventModelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnly]
    queryset = Event.objects.all()
    model = Event
    serializer_class = EventSerializer

from django.core.mail import EmailMessage, send_mail
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from eventManagers import settings
from event_manager.models import Event
from event_manager.serializers import EventSerializer, EventCreateSerializer, EventHandlersSerializer
from user.models import User


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



    def get_queryset(self):
        queryset = Event.objects.all()
        title = self.request.GET.get("title")
        description = self.request.GET.get("description")
        date = self.request.GET.get("date")
        location = self.request.GET.get("location")
        organizer = self.request.GET.get("organizer")
        if title:
            queryset = queryset.filter(
                title__icontains=title
            )
        if description:
            queryset = queryset.filter(
                description__icontains=description
            )
        if date:
            queryset = queryset.filter(
                date__icontains=date
            )
        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        if organizer:
            queryset = queryset.filter(
               organizer=organizer
            )

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                description="Filter by title",
            ),
            OpenApiParameter(
                name="description",
                type=OpenApiTypes.STR,
                description="Filter by wine description",
            ),
            OpenApiParameter(
                name="date",
                type=OpenApiTypes.STR,
                description="Filter by wine date",
            ),
            OpenApiParameter(
                name="location",
                type=OpenApiTypes.STR,
                description="Filter by location",
            ),
            OpenApiParameter(
                name="organizer",
                type=OpenApiTypes.INT,
                description="Filter by organizer",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """filtering for query_params for events by: title, description , date , location , organizer """
        return super().list(request, *args, **kwargs)


def sent_email(email : str , header_text : str , body_text : str):
    subject = header_text
    txt = body_text
    recipient_list = [email,]
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        txt,
        from_email,
        recipient_list,
        fail_silently=False,
    )

class EventsHandler(UpdateAPIView , DestroyAPIView  ,  GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventHandlersSerializer

    def put(self , request , *args, **kwargs):
        partial = kwargs.pop('partial', False)
        member_id = request.user.id
        instance = self.get_object()
        if not instance.members.filter(id=request.user.id).exists():
            instance.members.add(member_id)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            user = User.objects.get(id=request.user.id)
            sent_email(
                email = user.email,
                header_text=f"Event! {instance.title}",
                body_text=f"You are registered for the event that conducts {instance.organizer} on the {instance.date}. Location is {instance.location}" )

            return Response({f"message": "User joined for event"}, status=status.HTTP_200_OK)
        return Response({"error": "user already exist"}, status=status.HTTP_409_CONFLICT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.members.filter(id=request.user.id).exists():
            instance.members.remove(request.user)
            instance.save()
            return Response({"message": "User Deleted for event"}, status=status.HTTP_200_OK)

        return Response({"error": "user not found"}, status=status.HTTP_400_BAD_REQUEST)

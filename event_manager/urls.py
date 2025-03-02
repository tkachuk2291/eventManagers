from event_manager.views import EventModelViewSet, EventsHandler
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("event", EventModelViewSet, basename="event")



urlpatterns = [path("", include(router.urls)),
               path("event-register/<pk>/", EventsHandler.as_view()),
               ]

app_name = "event"

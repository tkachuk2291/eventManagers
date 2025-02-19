from event_manager.views import EventModelViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("event", EventModelViewSet, basename="event")

urlpatterns = [path("", include(router.urls))]

app_name = "event"

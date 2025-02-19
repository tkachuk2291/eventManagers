from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import UsermodelViewSet

router = DefaultRouter()

router.register("user_account", UsermodelViewSet, basename="user_account")

urlpatterns = [path("", include(router.urls))]

app_name = "user"

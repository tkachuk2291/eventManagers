from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import UsermodelViewSet

router = DefaultRouter()

router.register("user_account", UsermodelViewSet, basename="user_account")

urlpatterns = [path("", include(router.urls)),
               path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('user/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
               ]

app_name = "user"

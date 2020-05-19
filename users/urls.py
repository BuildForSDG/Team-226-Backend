from django.urls import include, path
from rest_framework import routers

from .views import CreateUserView, UserViewSet

router = routers.DefaultRouter()
router.register(r"user", UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("auth/register/", CreateUserView.as_view(), name="user-register"),
    path("", include((router.urls, "users"), namespace="users")),
]

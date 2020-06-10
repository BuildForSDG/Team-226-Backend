from django.urls import include, path
from rest_framework import routers

from .views import (
    AddUserCategory,
    CreateUserView,
    DeleteUserCategory,
    UserViewSet,
)

router = routers.DefaultRouter()
router.register(r"user", UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("auth/register/", CreateUserView.as_view(), name="user-register"),
    path("", include((router.urls, "users"), namespace="users")),
    path("user/category/add/", AddUserCategory.as_view(), name="user_add_category"),
    path(
        "user/category/delete/<int:category_id>/",
        DeleteUserCategory.as_view(),
        name="user_delete_category",
    ),
]

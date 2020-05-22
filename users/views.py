from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status, viewsets, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from resources.models import UserCategory
from resources.serializers import UserCategorySerializer
from .models import User
from .serializers import UserSerializer, UserSerializerWithToken


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_created")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def retrieve(self, request, pk=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CreateUserView(APIView):
    """
    API endpoint that allows visitors to create accounts.
    For signup
    """

    permission_classes = (permissions.AllowAny,)
    parser_classes = (MultiPartParser,)
    response = '{"response": "success", "message": "user created succesfully"}'

    @swagger_auto_schema(
        request_body=UserSerializerWithToken,
        query_serializer=UserSerializer,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="auth_create_user",
        operation_description="""
            Create a new user
            Accepts the following POST parameters:
                email* and password* are required create the new user
        """,
    )
    def post(self, request):
        user = request.data
        if not user:
            return Response({"response": "error", "message": "No data found"})

        serializer = UserSerializerWithToken(data=user)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"response": "success", "message": "user created succesfully"})


class AddUserCategory(APIView):
    """
        API endpoint that allows users to add Categories to their list
    """

    @swagger_auto_schema(
        request_body=UserCategorySerializer,
        responses={"200": "", "400": "Bad Request"},
        security=[],
        operation_id="auth_create_user",
        operation_description="""
                Add an existing category to a users category list
            """,
    )
    def post(self, request):
        serializer = UserCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            {"response": "success", "message": "category added succesfully"}
        )


class DeleteUserCategory(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
        API endpoint that allows users to remove a category from a user's category list
    """

    def get_object(self):
        user_category = UserCategory.objects.get_user_category(
            self.request.user.id, self.kwargs.get("category_id")
        )
        print(user_category)
        print(self.request.user.id)
        if user_category.exists():
            return user_category
        else:
            raise Http404("Category not found")

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

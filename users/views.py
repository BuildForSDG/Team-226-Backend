from django.core import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

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
    response = '{"response": "success", "message": "user created succesfully"}'

    @swagger_auto_schema(
        request_body=UserSerializerWithToken,
        query_serializer=UserSerializerWithToken,
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
        user_data = request.data
        if not user_data:
            return Response({"response": "error", "message": "No data found"})

        serializer = UserSerializerWithToken(data=user_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user_data["username"] = user.username
        return Response(
            {
                "response": "success",
                "message": "user created succesfully",
                "data": user_data,
            }
        )

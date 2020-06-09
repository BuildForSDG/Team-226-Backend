from collections import OrderedDict

from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from resources.models import Land, Category, Post, List, ListPost, Comment
from resources.permissions import ResourcesAnonymousAccessPermission
from resources.serializers import (
    LandSerializer,
    LandImageSerializer,
    CategorySerializer,
    PostSerializer,
    PostImageSerializer,
    CategorySerializerForDocs,
    LandSerializerForDocs,
    PostSerializerForDocs,
    ListSerializer,
    ListSerializerForDocs,
    ListPostSerializer,
    ListPostSerializerForDocs,
    CommentSerializer,
    CommentSerializerForDocs,
    CommentImageSerializer,
)


class LandListCreate(generics.ListCreateAPIView):

    """API endpoint that allows users to create and view list of lands."""

    response = '{"response": "success", "message": "land created succesfully"}'
    serializer_class = LandSerializer

    permission_classes = [IsAuthenticated | ResourcesAnonymousAccessPermission]

    def get_queryset(self):
        return Land.objects.get_all_lands(self.request.data.get("owner"))

    def get(self, request, *args, **kwargs):
        """GET all lands posted by all users."""
        response_obj = super(LandListCreate, self).get(request, *args, **kwargs)
        response_obj.data["results"] = self.build_land_obj(response_obj.data["results"])
        return response_obj

    @swagger_auto_schema(
        request_body=LandSerializerForDocs,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="resource_create_land",
        operation_description="""
                                Create a Land Entity
                                """,
    )
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data["owner"] = request.user.id
        return super(LandListCreate, self).post(request, *args, **kwargs)

    @staticmethod
    def build_land_obj(response_array):
        response_obj = []
        for value_obj in response_array:
            image_serializer = LandImageSerializer(
                Land.objects.get(id=value_obj.get("id")).land_images.all(), many=True
            )
            value_obj["images"] = image_serializer.data
            response_obj.append(value_obj)
        return response_obj


class CategoryListCreate(generics.ListCreateAPIView):

    """API endpoint that allows users to create and view list of categories."""

    response = '{"response": "success", "message": "category created succesfully"}'
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated | ResourcesAnonymousAccessPermission]

    def get_queryset(self):
        return Category.objects.get_all_categories(self.request.data.get("owner"))

    def get(self, request, *args, **kwargs):
        """GET all categories added by all users."""
        return super(CategoryListCreate, self).get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CategorySerializerForDocs,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="resource_create_category",
        operation_description="""Create a Category""",
    )
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data["created_by"] = request.user.id
        return super(CategoryListCreate, self).post(request, *args, **kwargs)


class LandUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LandSerializer

    def get_object(self):
        try:
            return Land.objects.get_land(self.kwargs.get("land_id"))
        except Land.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        request_body=LandSerializerForDocs,
        responses={"200": "", "400": "Bad Request"},
        security=[],
        operation_id="resource_update_delete_land",
        operation_description="""Update or delete a land""",
    )
    def put(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data["owner"] = request.user.id
        return super(LandUpdateDelete, self).put(request, *args, **kwargs)


class PostUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer

    def get_object(self):
        try:
            return Post.objects.get_post(self.kwargs.get("post_id"))
        except Post.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        request_body=PostSerializer,
        responses={"200": "", "400": "Bad Request"},
        security=[],
        operation_id="resource_update_delete_post",
        operation_description="""
                Update or delete a Post
        """,
    )
    def put(self, request, *args, **kwargs):
        return super(PostUpdateDelete, self).put(request, *args, **kwargs)


class ListingsUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ListSerializer

    def get_object(self):
        try:
            return List.objects.get_list(self.kwargs.get("list_id"))
        except Post.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        request_body=ListSerializer,
        responses={"200": "", "400": "Bad Request"},
        security=[],
        operation_id="resource_update_delete_list",
        operation_description="""Update or delete a List""",
    )
    def put(self, request, *args, **kwargs):
        return super(ListingsUpdateDelete, self).put(request, *args, **kwargs)


class UploadImages(generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = LandImageSerializer

    response = '{"response": "success", "message": "image uploaded succesfully"}'

    @swagger_auto_schema(
        request_body=LandImageSerializer,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="resource_upload_images",
        operation_description="""
                    Upload images
                    @pathVariable type should be (post or land or comment) depending on what the images
                    are post for
                """,
    )
    def post(self, request, *args, **kwargs):
        image_type = self.kwargs.get("type")
        if image_type not in ("land", "post", "comment"):
            return Response("error", status.HTTP_400_BAD_REQUEST)
        upload_for = request.data.get("upload_for", None)
        if upload_for is not None:
            for image in dict(request.data.lists()).get("image", []):
                image_serializer = None
                if image_type == "land":
                    image_serializer = LandImageSerializer(
                        data={"image": image, "upload_for": upload_for}
                    )
                elif image_type == "post":
                    image_serializer = PostImageSerializer(
                        data={"image": image, "upload_for": upload_for}
                    )
                elif image_type == "comment":
                    image_serializer = CommentImageSerializer(
                        data={"image": image, "upload_for": upload_for}
                    )
                image_serializer.is_valid(True)
                image_serializer.save()
            return Response("upload successful")
        else:
            return Response("upload_for field missing", status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_user_land_list(request):
    """GET ALL LANDS POSTED BY A USER."""
    serializer = LandSerializer(
        instance=Land.objects.get_all_lands(request.user.id), many=True,
    )
    return Response(serializer.data)


@api_view(["GET"])
def get_user_post_list(request):
    """GET ALL POST CREATED BY A USER."""
    serializer = PostSerializer(
        instance=Post.objects.get_all_posts(request.user.id), many=True,
    )
    return Response(serializer.data)


@api_view(["GET"])
def get_user_listing_list(request):
    """GET ALL LISTINGS CREATED BY A USER."""
    serializer = ListSerializer(
        instance=List.objects.get_all_posts(request.user.id), many=True,
    )
    return Response(serializer.data)


class PostListCreate(generics.ListCreateAPIView):

    """API endpoint that allows users to create and get list of posts."""

    response = '{"response": "success", "message": "post created succesfully"}'
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated | ResourcesAnonymousAccessPermission]

    def get_queryset(self):
        return Post.objects.get_all_posts(self.request.data.get("created_by"))

    def get(self, request, *args, **kwargs):
        """GET all post created by all users."""
        response_obj = super(PostListCreate, self).get(request, *args, **kwargs)
        response_obj.data["results"] = self.build_post_obj(response_obj.data["results"])
        return response_obj

    @swagger_auto_schema(
        request_body=PostSerializerForDocs,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="resource_create_post",
        operation_description="""
                Create a Post Entity
            """,
    )
    def post(self, request, *args, **kwargs):
        if type(request.data) is not dict:
            request.data._mutable = True
        request.data["created_by"] = request.user.id
        return super(PostListCreate, self).post(request, *args, **kwargs)

    @staticmethod
    def build_post_obj(response_array):
        response_obj = []
        for value_obj in response_array:
            image_serializer = PostImageSerializer(
                Post.objects.get(id=value_obj.get("id")).post_images.all(), many=True
            )
            value_obj["images"] = image_serializer.data
            response_obj.append(value_obj)
        return response_obj


class ListingsListCreate(generics.ListCreateAPIView):

    """API endpoint that allows users to create and get list of listings."""

    response = '{"response": "success", "message": "post created succesfully"}'
    serializer_class = ListSerializer

    def get_queryset(self):
        return List.objects.get_all_lists(self.request.data.get("created_by"))

    def get(self, request, *args, **kwargs):
        """GET all list created by all users."""
        return super(ListingsListCreate, self).get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ListSerializerForDocs,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="resource_create_list",
        operation_description="""
                Create a List Entity
            """,
    )
    def post(self, request, *args, **kwargs):
        if type(request.data) is not dict:
            request.data._mutable = True
        request.data["created_by"] = request.user.id
        return super(ListingsListCreate, self).post(request, *args, **kwargs)


class ListAddPost(generics.CreateAPIView):

    """API endpoint that allows users to add his post to a listing"""

    serializer_class = ListPostSerializer
    response = '{"response": "success", "message": "post add to list succesfully"}'

    @swagger_auto_schema(
        request_body=ListPostSerializerForDocs,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="resource_add_post_to_list",
        operation_description="""Add post to list""",
    )
    def post(self, request, *args, **kwargs):
        if type(request.data) is not dict:
            request.data._mutable = True
        request.data["user"] = request.user.id
        return super(ListAddPost, self).post(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     print(serializer.validated_data)
    #     serializer.save(user=self.request.user.id)


class ListingsPost(generics.ListAPIView):
    response = '{"response": "success", "message": "successful"}'
    serializer_class = ListPostSerializer

    def get_queryset(self):
        return List.objects.get_all_post_in_list(self.kwargs["list_id"])

    def get(self, request, *args, **kwargs):
        """GET ALL POST IN A LIST."""
        return super(ListingsPost, self).get(request, *args, **kwargs)


class ListDeletePost(APIView):
    response = '{"response": "success", "message": "post deleted succesfully"}'

    @staticmethod
    @swagger_auto_schema(
        request_body=ListPostSerializerForDocs,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="resource_delete_post_from_list",
        operation_description="""Delete post from list""",
    )
    def delete(request, *args, **kwargs):
        if type(request.data) is not dict:
            request.data._mutable = True
        request.data.update({"user": request.user.id})
        data = request.data
        qs = ListPost.objects.get_list_post(
            data.get("user"), data.get("list"), data.get("post")
        )
        if qs.exists():
            qs.delete()
            return Response({"response": "Delete successful"})
        else:
            return Response(
                {"response": "User doesn't have post assigned to list"},
                status.HTTP_400_BAD_REQUEST,
            )


class CommentListCreate(generics.ListCreateAPIView):

    """API endpoint that allows users to comment and get list of comments."""

    response = '{"response": "success", "message": "comment created succesfully"}'
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated | ResourcesAnonymousAccessPermission]

    def get_queryset(self):
        return Comment.objects.get_comments_for_post(self.kwargs.get("post_id"))

    def get(self, request, *args, **kwargs):
        """GET all comments for a post."""

        response_obj = super(CommentListCreate, self).get(request, *args, **kwargs)
        response_obj.data["results"] = self.build_comment_reply_obj(
            response_obj.data["results"]
        )
        return response_obj

    @swagger_auto_schema(
        request_body=CommentSerializerForDocs,
        responses={"200": response, "400": "Bad Request"},
        security=[],
        operation_id="resource_create_comment",
        operation_description="""
                Comment under a Post
            """,
    )
    def post(self, request, *args, **kwargs):
        if type(request.data) is not dict:
            request.data._mutable = True
        request.data["created_by"] = request.user.id
        request.data["post"] = self.kwargs.get("post_id")
        return super(CommentListCreate, self).post(request, *args, **kwargs)

    @staticmethod
    def build_comment_reply_obj(response_array):
        obj = OrderedDict()
        for value_obj in response_array:
            image_serializer = CommentImageSerializer(
                Comment.objects.get(id=value_obj.get("id")).comment_images.all(),
                many=True,
            )
            value_obj["images"] = image_serializer.data
            if value_obj.get("reply_to") is None:
                obj[value_obj.get("id")] = value_obj
                obj[value_obj.get("id")]["replies"] = []
            else:
                if "replies" not in obj[value_obj.get("reply_to")]:
                    obj[value_obj.get("reply_to")]["replies"] = []
                obj[value_obj.get("reply_to")]["replies"].append(value_obj)
        return obj

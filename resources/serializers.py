from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from resources.constants import Constants
from resources.models import (
    Category,
    Comment,
    CommentImage,
    Land,
    LandImage,
    List,
    ListPost,
    Post,
    PostImage,
    UserCategory,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        """ Category serializer meta properties """

        model = Category
        fields = ["name", "slug", "created_by"]
        read_only_fields = ["date_created", "date_updated"]


class CategorySerializerForDocs(serializers.ModelSerializer):
    class Meta(CategorySerializer.Meta):
        """ category serializer for docs meta properties """

        fields = ["name", "slug"]


class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        """ user category serializer meta properties """

        model = UserCategory
        fields = "__all__"


class LandSerializer(serializers.ModelSerializer):
    class Meta:
        """ land serializer meta properties """

        model = Land
        fields = [
            "id",
            "title",
            "cost",
            "for_type",
            "size",
            "size_unit_measurement",
            "location",
            "visibility",
            "owner",
            "currency",
            "lease_rate_periodicity",
            "date_created",
            "date_updated",
        ]
        read_only_fields = ["date_created", "date_updated"]

    def is_valid(self, raise_exception=False):
        if self.initial_data.get("for_type") == Constants.LEASE:
            if int(self.initial_data.get("cost", 0)) <= 0:
                raise ValidationError(
                    {"message", "land type cost must be greater than 0 for leasing"}
                )
            if self.initial_data.get("lease_rate_periodicity") is None:
                raise ValidationError(
                    {"message", "land type leasing interval for cost must be provided"}
                )
        else:
            self.initial_data["cost"] = 0
            self.initial_data["lease_rate_periodicity"] = ""
        super(LandSerializer, self).is_valid(raise_exception)


class LandSerializerForDocs(serializers.ModelSerializer):
    class Meta(LandSerializer.Meta):
        """ land serializer for docs meta properties """

        import copy

        fields = copy.deepcopy(LandSerializer.Meta.fields)
        fields.remove("owner")


class LandImageSerializer(serializers.ModelSerializer):
    class Meta:
        """ land image serializer meta properties """

        model = LandImage
        exclude = ["upload_for"]
        read_only_fields = ["date_created", "date_updated"]


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        """ post image serializer meta properties """

        model = PostImage
        exclude = ["upload_for"]
        read_only_fields = ["date_created", "date_updated"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        """ post serializer meta properties """

        model = Post
        fields = "__all__"


class PostSerializerForDocs(serializers.ModelSerializer):
    class Meta(PostSerializer.Meta):
        """ post serializer for docs meta properties """

        fields = None
        exclude = ["created_by"]


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        """ list serializer meta properties """

        model = List
        fields = "__all__"


class ListSerializerForDocs(serializers.ModelSerializer):
    class Meta(ListSerializer.Meta):
        """ list serializer for docs meta properties """

        fields = None
        exclude = ["created_by"]


class ListPostSerializer(serializers.ModelSerializer):
    class Meta:
        """ list post serializer meta properties """

        model = ListPost
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        user = self.initial_data.get("user")
        post_exist = Post.objects.get_user_post(
            user, self.initial_data.get("post")
        ).exists()
        list_exist = List.objects.get_user_list(
            user, self.initial_data.get("list")
        ).exists()
        if post_exist and list_exist:
            super(ListPostSerializer, self).is_valid()
        else:
            raise ValidationError("Either post or list does not belong to user")


class ListPostSerializerForDocs(serializers.ModelSerializer):
    class Meta(ListPostSerializer.Meta):
        """ list post serializer for docs meta properties """

        fields = None
        exclude = ["user"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:

        """DOC STRING"""

        fields = [
            "id",
            "created_by",
            "post",
            "text",
            "date_created",
            "date_updated",
            "reply_to",
        ]
        model = Comment


class CommentSerializerForDocs(serializers.ModelSerializer):
    class Meta(CommentSerializer.Meta):

        """DOC STRING"""

        fields = None
        exclude = ["created_by", "post", "date_updated", "date_created"]


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        """DOC STRING"""

        model = CommentImage
        fields = ["id", "image"]
        read_only_fields = ["date_created", "date_updated"]

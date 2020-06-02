from django.urls import path

from resources.views import (
    CategoryListCreate,
    LandListCreate,
    LandUpdateDelete,
    ListAddPost,
    ListDeletePost,
    ListingsListCreate,
    ListingsPost,
    ListingsUpdateDelete,
    PostListCreate,
    PostUpdateDelete,
    UploadImages,
    get_user_land_list,
    get_user_post_list,
)

urlpatterns = [
    path("land/", LandListCreate.as_view(), name="create_or_get_lands"),
    path("land/<int:land_id>/", LandUpdateDelete.as_view(), name="update_land"),
    path("user/land/", get_user_land_list, name="get_lands"),
    path("post/", PostListCreate.as_view(), name="create_or_get_post"),
    path("post/<int:post_id>/", PostUpdateDelete.as_view(), name="update_post"),
    path("user/post/", get_user_post_list, name="get_posts"),
    path("list/", ListingsListCreate.as_view(), name="create_or_get_list"),
    path("list/<int:list_id>/", ListingsUpdateDelete.as_view(), name="update_list"),
    path("list/<int:list_id>/post/", ListingsPost.as_view(), name="list_post"),
    path("list/add/post/", ListAddPost.as_view(), name="add_post_to_list"),
    path("list/delete/post/", ListDeletePost.as_view(), name="delete_post_from_list"),
    path("user/list/", get_user_post_list, name="get_list"),
    path("category/", CategoryListCreate.as_view(), name="create_or_get_categories"),
    path("upload/<str:type>/images/", UploadImages.as_view(), name="upload_images"),
]

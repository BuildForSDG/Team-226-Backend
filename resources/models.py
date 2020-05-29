from django.db import models

from resources.constants import Constants
from resources.querysets import (
    LandQuerySet,
    CategoryQuerySet,
    UserCategoryQuerySet,
    PostQuerySet,
    ListQuerySet,
    ListPostQuerySet,
)
from users.models import User


class Category(models.Model):
    name = models.CharField(verbose_name="Category name", max_length=155, unique=True)
    slug = models.SlugField(
        verbose_name="Category slug(from name)", max_length=255, blank=True
    )
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    objects = CategoryQuerySet.as_manager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = self.name
        super(Category, self).save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def __str__(self):
        return self.name


class Land(models.Model):
    title = models.CharField(verbose_name="Land title", max_length=255, unique=True,)
    cost = models.FloatField(verbose_name="Cost of land", max_length=100, blank=True)
    for_type = models.CharField(
        verbose_name="Land listing type(free or rent)",
        max_length=30,
        choices=Constants.FOR_TYPE,
        default=Constants.LEASE,
    )
    size = models.FloatField(verbose_name="Land size")
    size_unit_measurement = models.CharField(
        verbose_name="Land size measurement type",
        max_length=30,
        choices=Constants.SIZE_TYPE,
        default=Constants.METERS,
    )
    location = models.CharField(verbose_name="Land location", max_length=255)
    visibility = models.CharField(
        verbose_name="Visible to",
        max_length=30,
        choices=Constants.VISIBILITY_TYPE,
        default=Constants.PUBLIC,
    )
    owner = models.ForeignKey(
        "users.User", verbose_name="Author linked to", on_delete=models.CASCADE
    )
    currency = models.CharField(
        max_length=10,
        verbose_name="Currency",
        choices=Constants.CURRENCIES,
        default=Constants.XAF,
    )
    lease_rate_periodicity = models.CharField(
        verbose_name="Lease Rate Periodicity",
        max_length=10,
        choices=Constants.LEASE_RATE_PERIODICITY,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = LandQuerySet.as_manager()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class List(models.Model):
    title = models.CharField(verbose_name="List title", max_length=255)
    description = models.TextField(verbose_name="Description of the List", blank=True)
    cover_image = models.ImageField(verbose_name="Cover image", blank=True)
    created_by = models.ForeignKey(
        User, verbose_name="Author linked to", on_delete=models.CASCADE
    )
    visibility = models.CharField(
        verbose_name="Visible to",
        max_length=30,
        choices=Constants.VISIBILITY_TYPE,
        default=Constants.PUBLIC,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = ListQuerySet.as_manager()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(verbose_name="Post title", max_length=200)
    slug = models.SlugField(
        verbose_name="Post slug(from title)", max_length=255, unique=True
    )
    description = models.TextField(verbose_name="Description of the post", blank=True)
    video_link = models.TextField(verbose_name="Post video link", blank=True)
    created_by = models.ForeignKey(
        "users.User",
        verbose_name="Author linked to",
        on_delete=models.CASCADE,
        related_name="Author",
    )
    visibility = models.CharField(
        verbose_name="Visible to",
        max_length=30,
        choices=Constants.VISIBILITY_TYPE,
        default=Constants.PUBLIC,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class ListPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="listing")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")

    objects = ListPostQuerySet.as_manager()

    class Meta:
        unique_together = ["list", "post"]

    def __str__(self):
        return "Post: {} listed in {}".format(self.post.title, self.list.title)


class Comment(models.Model):
    text = models.TextField(verbose_name="Comment text")
    image = models.TextField(verbose_name="Comment image", blank=True)
    user = models.ForeignKey(
        "users.User", verbose_name="Author linked to", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "Post", verbose_name="Post linked to", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["text"]

    def __str__(self):
        return self.text


class LandImage(models.Model):
    image = models.ImageField(
        verbose_name="Image", upload_to="land_image_uploads/", blank=True
    )
    upload_for = models.ForeignKey(
        Land,
        verbose_name="Land Linked to",
        related_name="land_images",
        on_delete=models.CASCADE,
    )

    class Meta:
        pass

    def __str__(self):
        return self.image.name


class PostImage(models.Model):
    image = models.ImageField(
        verbose_name="Image", upload_to="post_image_uploads/", blank=True
    )
    upload_for = models.ForeignKey(
        Post,
        verbose_name="Post Linked to",
        related_name="post_images",
        on_delete=models.CASCADE,
    )

    class Meta:
        pass

    def __str__(self):
        return self.image.name


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    objects = UserCategoryQuerySet.as_manager()

    class Meta:
        pass

    def __str__(self):
        return "User: {}, Category: {}".format(self.user.first_name, self.category.name)

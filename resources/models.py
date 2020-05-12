from django.db import models

PRIVATE = "PR"
PUBLIC = "PU"
VISIBILITY_TYPE = [(PRIVATE, "private"), (PUBLIC, "public")]

METERS = "M"
KILOMETERS = "KM"
MILES = "ML"
SIZE_TYPE = [(METERS, "metres"), (KILOMETERS, "kilometres"), (MILES, "miles")]

FREE = "FR"
LEASE = "LE"
FOR_TYPE = [(FREE, "for free"), (LEASE, "for leasing")]


class Category(models.Model):
    name = models.CharField(verbose_name="Category name", max_length=155, unique=True)
    slug = models.SlugField(
        verbose_name="Category slug(from name)", max_length=255, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Land(models.Model):
    title = models.CharField(
        verbose_name="Land title(size + size_type + in + location)",
        max_length=255,
        unique=True,
    )
    cost = models.CharField(verbose_name="Cost of land", max_length=100, blank=True)
    for_type = models.CharField(
        verbose_name="Land listing type(free or rent)",
        max_length=30,
        choices=FOR_TYPE,
        default=LEASE,
    )
    size = models.CharField(verbose_name="Land size", max_length=30)
    size_type = models.CharField(
        verbose_name="Land size measurement type",
        max_length=30,
        choices=SIZE_TYPE,
        default=METERS,
    )
    location = models.CharField(verbose_name="Land location", max_length=255)
    images = models.TextField(verbose_name="Images of the land", blank=True)
    visibility = models.CharField(
        verbose_name="Visible to",
        max_length=30,
        choices=VISIBILITY_TYPE,
        default=PUBLIC,
    )
    owner = models.ForeignKey(
        "users.User", verbose_name="Author linked to", on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class List(models.Model):
    title = models.CharField(verbose_name="List title", max_length=255)
    description = models.TextField(verbose_name="Description of the List", blank=True)
    cover_image = models.TextField(verbose_name="Cover image", blank=True)
    user = models.ForeignKey(
        "users.User", verbose_name="Author linked to", on_delete=models.CASCADE
    )
    posts = models.ManyToManyField("Post", verbose_name="Posts of list", blank=True)
    visibility = models.CharField(
        verbose_name="Visible to",
        max_length=30,
        choices=VISIBILITY_TYPE,
        default=PUBLIC,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(verbose_name="Post title", max_length=200)
    slug = models.SlugField(
        verbose_name="Post slug(from title)", max_length=255, blank=True
    )
    description = models.TextField(verbose_name="Description of the post", blank=True)
    images = models.TextField(verbose_name="Post images", blank=True)
    video_link = models.TextField(verbose_name="Post video link", blank=True)
    user = models.ForeignKey(
        "users.User",
        verbose_name="Author linked to",
        on_delete=models.CASCADE,
        related_name="Author",
    )
    visibility = models.CharField(
        verbose_name="Visible to",
        max_length=30,
        choices=VISIBILITY_TYPE,
        default=PUBLIC,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


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
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["text"]

    def __str__(self):
        return self.text

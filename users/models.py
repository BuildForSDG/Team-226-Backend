from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    EMAIL = "EM"
    PHONE = "PH"
    PREF_CONTACT_CHOICES = [
        (EMAIL, "email"),
        (PHONE, "phone number"),
    ]

    email = models.EmailField(_("email address"), max_length=255, unique=True)
    username = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=80, blank=True)
    profile_photo = models.FileField(
        verbose_name="Profile picture", upload_to="user_photos/", blank=True
    )
    street = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=150, blank=True)
    pref_contact_method = models.CharField(
        verbose_name="Preferential Contact Method",
        choices=PREF_CONTACT_CHOICES,
        default=PHONE,
        max_length=3,
        blank=True,
    )
    # pref_categories = models.ManyToManyField(
    #     "resources.Category",
    #     related_name="pref_categories",
    #     verbose_name="Preferential Categories",
    # )
    date_joined = None
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        """ overiding str mehtod for class """

        ordering = ["email"]

    def __str__(self):
        """ overiding str mehtod for class """
        return "%s, %s" % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return "/users/user/%s" % self.username

    def make_username(self):
        self.username = self.first_name + "-" + self.last_name + str(self.pk)
        self.save()
        return self.username

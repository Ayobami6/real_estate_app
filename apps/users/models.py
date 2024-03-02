from django.db import models
from  django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
import uuid


class UserManager(BaseUserManager):
    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError({"email": _("Please enter a valid email address.")})


class User(AbstractBaseUser):
    object = UserManager()
    pkid = models.BigAutoField(primary_key=True,editable=False)
    id = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    first_name = models.CharField(max_length=80, verbose_name=_("First Name"), null=True, blank=True)
    last_name = models.CharField(max_length=80, verbose_name=_("Last Name"), null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name_plural = _("Users")
        verbose_name = _("User")

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.save()




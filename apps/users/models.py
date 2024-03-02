from django.db import models
from  django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(UserManager):
    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError({"email": _("Please enter a valid email address.")})

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValidationError({"email": _("Please enter a valid email address")})
        email = self.normalize_email(email)
        self.email_validator(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    objects = UserManager()
    obj_id = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    username = models.CharField(verbose_name=_("Username"), max_length=80, unique=True)
    first_name = models.CharField(max_length=80, verbose_name=_("First Name"), null=True, blank=True)
    last_name = models.CharField(max_length=80, verbose_name=_("Last Name"), null=True, blank=True)

    # USERNAME_FIELD = "email"

    class Meta:
        verbose_name_plural = _("CustomUsers")
        verbose_name = _("CustomUser")

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.save()




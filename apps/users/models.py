from django.db import models
from  django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    @staticmethod
    def email_validator(email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError({"email": _("Please enter a valid email address.")})



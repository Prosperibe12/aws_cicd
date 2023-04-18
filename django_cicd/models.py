from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken
from auditlog.registry import auditlog

from django_cicd.helpers.models import HelperModel


class MyUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(HelperModel, AbstractBaseUser, PermissionsMixin):
    """
    A base class implementing a fully featured User model with
    user-compliant permissions.
    Email and password are required. Other fields are optional.
    """
    type = (
        ('Proxy', 'Proxy'),
        ('Principal', 'Principal')
    )
    first_name = models.CharField(
        _("first name"), max_length=150, blank=False, null=False
    )
    last_name = models.CharField(
        _("last name"), max_length=150, blank=False, null=False
    )
    email = models.EmailField(
        _("email address"), blank=False, null=False, unique=True
    )
    phoneNumber = models.CharField(
        _("Phone Number"), max_length=50, blank=False, null=False
    )
    address = models.CharField(
        _("Address"), max_length=250, blank=False, null=False
    )
    city = models.CharField(_("City"), max_length=250, blank=False, null=False)
    lga = models.CharField(_("LGA"), max_length=250, blank=False, null=False)
    state = models.CharField(
        _("State"), max_length=250,
        blank=False, null=False
    )
    user_type = models.CharField(max_length=50, choices=type, default='')
    is_verified = models.BooleanField(
        _("Verified Status"),
        default=False,
        help_text=_("Designates that user is verified and can login."),
    )
    is_updated = models.BooleanField(
        _("Updated Status"),
        default=False,
        help_text=_("Designates that user has updated his/her account."),
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates that user can log to admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active."
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "user_type"]

    def __str__(self):
        return f'{self.first_name}'

    def tokens(self):
        tokens = RefreshToken.for_user(self)
        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token)
        }


auditlog.register(model=User, exclude_fields=['password', 'last_login'])

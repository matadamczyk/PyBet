from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = "server"
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    pycoins = models.FloatField(default=0.0)
    groups = models.ManyToManyField(Group, related_name="useraccount_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="useraccount_set", blank=True
    )

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserPickedOption(models.Model):
    class Meta:
        app_label = "server"
    matchTeams = models.CharField(max_length=25, null=True)
    selectedOption = models.CharField(max_length=255)
    date = models.DateField()
    selectedOdds = models.FloatField()
    stake = models.FloatField()
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True)

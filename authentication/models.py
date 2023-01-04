from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from department.models import Department
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        return user


# USER_TYPE_CHOICES = (
#     ('finance', 'Finance'),
#     ('procurement_committee', 'Procurement Committee'),
#     ('procurement_officer', 'Procurement Officer'),
#     ('ceo', 'CEO')
# )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=25, default='', null=True, blank=True)
    last_name = models.CharField(max_length=25, default='', null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, verbose_name="email")
    username = models.CharField(max_length=30, null=True, blank=True, default='')
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_head_department = models.BooleanField(default=False)
    is_procurement_officer = models.BooleanField(default=False)
    is_head_of_finance = models.BooleanField(default=False)
    is_procurement_committee = models.BooleanField(default=False)
    is_ceo = models.BooleanField(default=False)
    # user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=65, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def has_perm(self, app_label):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser

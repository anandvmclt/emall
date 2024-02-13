#emall/user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import Group, Permission

class UserScope():
    USER_SCOPES = [("ADMIN", "Administrator"), ("MANAGER", "Manager"),
                   ("USER", "User"), ("OTHER", "Other"), ]


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=True, max_length=254, verbose_name="email address", unique=True)
    mobile = models.CharField(max_length=12, null=True, blank=True, unique=True)
    user_scope = models.CharField(max_length=20, null=True, choices=UserScope.USER_SCOPES, default="USER")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.BooleanField(default=True) 
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group, blank=True, related_name="custom_users_groups")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="custom_users_permissions")

    def __str__(self):
        return str(self.username)
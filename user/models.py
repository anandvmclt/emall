#emall/user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import Group, Permission
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail

from django_rest_passwordreset.signals import reset_password_token_created


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
    


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    # email_html_message = render_to_string('email/user_reset_password.html', context)
    # email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    subject = 'Password reset'
    message = f'Hi {reset_password_token.user.username},  password reset token is : { reset_password_token.key}.'
    email_from = "suport@emall.com"
    recipient_list = [reset_password_token.user.email, ]
    send_mail( subject, message, email_from, recipient_list )

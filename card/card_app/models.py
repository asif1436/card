from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models

from django.utils import timezone

# class EventManager(models.Manager):
#
#     def get_queryset(self):
#         return super().get_queryset().filter(
#             timestamp__gte=timezone.now()-timezone.timedelta(minutes=5)
#         )

class MyUserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            #date_of_birth=date_of_birth
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            #date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """
    creating user by inheriting AbstractBaseUser
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_name = models.CharField(max_length=255, verbose_name="User Name",
                                 null=True,
                                 blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Card(models.Model):
    """
    Card Model.
    """
    card_title = models.CharField(max_length=100, null=True,
                                  verbose_name="Card Title")
    card_text = models.CharField(max_length=100, null=True,
                                 verbose_name="Card Text")
    card_status = models.BooleanField(default=True)
    card_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        :return: card title.
        """
        return self.card_title


class OTP(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        :return: user.
        """
        return str(self.user)

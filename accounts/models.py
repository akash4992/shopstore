from datetime import timedelta
from django.conf import settings

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have a username")
        user_obj = self.model(
            email = self.normalize_email(email),
            username=username
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,username=None, password=None):
        user = self.create_user(
                email,
                username=username,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(
                email,
                username=username,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True)
    username   = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=30,
                                  help_text='First Name of the user.')

    last_name = models.CharField(max_length=30,
                                 help_text='Last Name of the user.')
    is_active   = models.BooleanField(default=True) 
    staff       = models.BooleanField(default=False) 
    admin       = models.BooleanField(default=False) 
    timestamp   = models.DateTimeField(auto_now_add=True)
   

    USERNAME_FIELD = 'email' 
    
    REQUIRED_FIELDS = ['username'] 

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        The user is identified by their email address.
        '''

        return '%s %s' % (self.first_name, self.last_name)

    # ------------------------------------------------------------
    # get_short_name
    # ------------------------------------------------------------
    def get_short_name(self):
        '''
        The user is identified by their email address.
        '''

        return self.first_name
        


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active












class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
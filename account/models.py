from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


from .managers import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('name'), max_length = 250)
    email = models.EmailField(_('email'), unique=True)
    password = models.CharField(_('password'), max_length=300)
    is_active  = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_admin = models.BooleanField(_('admin'), default= False)
    is_superuser = models.BooleanField(_('superuser'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
        

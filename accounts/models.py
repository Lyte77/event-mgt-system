

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class UserManager(BaseUserManager):
     def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

     def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    is_organizer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    full_name = models.CharField(max_length=120,blank=True)
    country = CountryField(blank_label="(Select country)")
    phone = models.CharField(max_length=20,blank=True)
    about_organizer = models.TextField(blank=True,null=True,)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True,null=True)
    is_organizer = models.BooleanField(default=False) 
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.email }"
    
    @property
    def name(self):
        if self.full_name:
            return self.full_name
        return self.user.email 
    
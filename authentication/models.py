from enum import unique
from re import T
import uuid
from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
        )

        # save password + hashing
        user.set_password(password)
        # logic for dob
        user.firstname = firstname
        user.lastname = lastname
        user.user_type_choice = '4'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstname, lastname, password=None,**extra_fields):
        user = self.create_user(
            email,
            firstname,
            lastname,
            password=password,
        )
        user.is_admin = True
        user.user_type_choice = '1'  # Set user_type_choice as 'SuperUser'

        user.save(using=self._db)
        return user
        # return self.create_user(email, firstname, lastname, password, **extra_fields)



class User(AbstractBaseUser):
    
    choice = (("1", 'SuperUser'), ("2", 'Admin'),("3",'User'),("4",'ReadOnlyUSer'))
    user_type_choice = models.CharField(max_length=100, choices=choice)

    email = models.EmailField(verbose_name='email', max_length=200, unique=True, )
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS: list['firstname','lastname','dob','phone','address']
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def __str__(self):
        return self.firstname + " " + self.lastname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Profile(models.Model):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    Phone = models.CharField(max_length=30, null=True, blank=True)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        # breakpoint()
        first_name = kwargs['instance'].firstname
        last_name = kwargs['instance'].lastname
        user_profile = Profile.objects.create(first_name=first_name, last_name=last_name, user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
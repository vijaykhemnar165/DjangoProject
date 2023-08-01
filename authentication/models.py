from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group, Permission
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import Permission, Group



class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), username=username,)
        user.is_customer = True
        user.set_password(password)
        user.user_type_choice = '3'
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password=None):
        user = self.create_user(email, password=password, username=username)
        user.is_staff = True
        user.is_customer = True
        user.user_type_choice = '2'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, password=password, username=username)
        user.is_staff = True
        user.is_superuser=True
        user.is_customer = True
        user.user_type_choice = '1'
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    """
    Creates a customized database table for user using customized user manager
    """
    choice = (("1", 'SuperUser'), ("2", 'Admin'),("3",'Customer User'))
    user_type_choice = models.CharField(max_length=100, choices=choice)
    email = models.EmailField(verbose_name='email address',
                              max_length=255, unique=True,error_messages={
                                    'unique': ("A user with that username already exists."),
                                },)
    username = models.CharField(
                                max_length=150,
                                unique=False,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]
    objects = UserProfileManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.user_type_choice == '1':
            return True
        elif self.user_type_choice == '2':
            crud_permissions = ['can_add_organisation','can_change_organisation', 'can_delete_organisation', 'can_view_organisation','can_add_site', 'can_change_site', 'can_delete_site', 'can_view_site', ]
            return self.user.user_permissions.add(*Permission.objects.filter(codename__in=crud_permissions))

        elif self.user_type_choice == '3':
            crud_permissions = ['can_view_organisation', 'can_view_site']
            return self.user.user_permissions.add(*Permission.objects.filter(codename__in=crud_permissions))
        return False


    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        super_admin_permissions = [
            Permission.objects.get(codename='delete_organisation'),
            Permission.objects.get(codename='view_organisation'),

            Permission.objects.get(codename='add_site'),
            Permission.objects.get(codename='change_site'),
            Permission.objects.get(codename='delete_site'),
            Permission.objects.get(codename='view_site'),

        ]

        tenant_user_permissions = [
            Permission.objects.get(codename='add_organisation'),
            Permission.objects.get(codename='change_organisation'),
            Permission.objects.get(codename='delete_organisation'),
            Permission.objects.get(codename='view_organisation'),

            Permission.objects.get(codename='add_site'),
            Permission.objects.get(codename='change_site'),
            Permission.objects.get(codename='delete_site'),
            Permission.objects.get(codename='view_site'),

        ]

        customer_user_permissions = [
            Permission.objects.get(codename='view_organisation'),
            Permission.objects.get(codename='view_site'),
        ]

        if self.user_type_choice == '1':  # Super Admin
            super_admin_group, _ = Group.objects.get_or_create(name='Super Admin')
            self.groups.set([super_admin_group])
            self.user_permissions.set(super_admin_permissions)

        elif self.user_type_choice == '2':  # Tenant User
            tenant_user_group, _ = Group.objects.get_or_create(name='Tenant User')
            self.groups.set([tenant_user_group])
            self.user_permissions.set(tenant_user_permissions)

        elif self.user_type_choice == '3':  # Customer User
            customer_user_group, _ = Group.objects.get_or_create(name='Customer User')
            self.groups.set([customer_user_group])
            self.user_permissions.set(customer_user_permissions)

class UserInvitation(models.Model):
    ACCEPTED = 'accepted'
    EXPIRED = 'expired'
    PENDING = 'pending'

    STATUS_CHOICES = (
        (ACCEPTED, 'Accepted'),
        (EXPIRED, 'Expired'),
        (PENDING, 'Pending'),
    )

    ROLE_TENANT_ADMIN = 'tenant_admin'
    ROLE_USER = 'user'

    ROLE_CHOICES = (
        (ROLE_TENANT_ADMIN, 'Tenant Admin'),
        (ROLE_USER, 'User'),
    )

    email = models.CharField(max_length=150, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    invited_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)

    

# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, email, firstname, lastname, password=None,**extra_fields):
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         user = self.model(
#             email=self.normalize_email(email),
#             firstname=firstname,
#             lastname=lastname,
#         )
#
#         # save password + hashing
#         user.set_password(password)
#         # logic for dob
#         user.firstname = firstname
#         user.lastname = lastname
#         user.user_type_choice = '4'
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, firstname, lastname, password=None,**extra_fields):
#         user = self.create_user(
#             email,
#             firstname,
#             lastname,
#             password=password,
#         )
#         user.is_admin = True
#         user.user_type_choice = '1'  # Set user_type_choice as 'SuperUser'
#
#         user.save(using=self._db)
#         return user
#         # return self.create_user(email, firstname, lastname, password, **extra_fields)
#
#
#
# class User(AbstractBaseUser):
#
#     choice = (("1", 'SuperUser'), ("2", 'Admin'),("3",'User'),("4",'ReadOnlyUSer'))
#     user_type_choice = models.CharField(max_length=100, choices=choice)
#
#     email = models.EmailField(verbose_name='email', max_length=200, unique=True, )
#     firstname = models.CharField(max_length=200)
#     lastname = models.CharField(max_length=200)
#     is_admin = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['firstname', 'lastname']
#
#     def __str__(self):
#         return self.firstname + " " + self.lastname
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Profile(models.Model):
    username = models.CharField(max_length=150, null=True, blank=True)
    # last_name = models.CharField(max_length=100, null=True, blank=True)
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
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
        username = kwargs['instance'].username
        # last_name = kwargs['instance'].lastname
        user_profile = Profile.objects.create(username=username, user=kwargs['instance'])


post_save.connect(create_profile, sender=UserProfile)












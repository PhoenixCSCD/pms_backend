import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, gender, date_of_birth, phone_number,  password=None):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, gender, date_of_birth, phone_number, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            password=password
        )
        user.is_staff = True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)

    avatar = models.FilePathField(path="media/avatars/", null=True)

    branches = models.ManyToManyField(Branch, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'date_of_birth', 'phone_number']

    objects = UserManager()


class Allergy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)


class Drug(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=250)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
    cost_price_per_pack = models.DecimalField(max_digits=19, decimal_places=2)
    quantity_per_pack = models.IntegerField(default=1)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file = models.ImageField(upload_to='images')
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(pre_delete, sender=Image)
def delete_image_on_disk(sender, instance, **_kwargs):
    instance.file.delete(False)

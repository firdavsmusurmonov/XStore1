from django.db import models
from django.contrib.auth.models import AbstractUser


# from doctor.utils import generate_unique_slug
# Create your models here.

def get_avatar(instance, filename):
    return "users/%s" % (filename)


class Customuser(AbstractUser):
    GENDER_CHOICES = (
        ('man', 'Man'),
        ('woman', 'Woman')
    )
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    fullname = models.CharField(max_length=150, blank=True, null=True)
    smscode = models.IntegerField(default=0)
    complete = models.IntegerField(default=0)
    phone = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=get_avatar, default='users/default.png')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50, null=True, blank=True)
    birth_date = models.DateField(default=None, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    langtude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)


class Region(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

from email.mime import image
from pyexpat import model
from unicodedata import category
from django.db import models

from account.models import Customuser


# Create your models here.


def get_image(instance, filename):
    return "users/%s" % (filename)


def get_story(instance, filename):
    return "users/%s" % (filename)


def get_category(instance, filename):
    return "users/%s" % (filename)


def get_storyved(instance, filename):
    return "users/%s" % (filename)


class Category(models.Model):
    name = models.CharField(max_length=55, null=True, blank=True)
    image = models.ImageField(upload_to=get_category, default='users/default.png')
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


class Color(models.Model):
    color = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.color


class Image(models.Model):
    image = models.ImageField(upload_to=get_image, default='users/default.png')
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE, null=True)


class Infomation(models.Model):
    style = models.CharField(max_length=55, null=True, blank=True)
    color = models.ManyToManyField(Color, related_name='information')
    price = models.IntegerField(default=0)
    releaseDate = models.DateField(default=None, null=True, blank=True)

    def __str__(self):
        return str(self.style)


class Allsize(models.Model):
    size = models.IntegerField(default=0)

    def __str__(self):
        return str(self.size)


class Product(models.Model):
    name = models.CharField(max_length=55, null=True, blank=True)
    brend = models.CharField(max_length=55, null=True, blank=True)
    # price = models.IntegerField(default=0)
    color = models.ManyToManyField(Color, related_name='product')
    title = models.TextField(max_length=255, null=True, blank=True)
    desc = models.TextField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, related_name="user_category", null=True, blank=True,
                                 on_delete=models.CASCADE)
    information = models.ForeignKey(Infomation, related_name="user_information", null=True, blank=True,
                                    on_delete=models.CASCADE)
    justDropped = models.BooleanField(default=False)
    mostPopular = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class ProductPrice(models.Model):
    size = models.ForeignKey(Allsize, related_name="alsize", null=True, blank=True,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="produk", null=True, blank=True,
                                on_delete=models.SET_NULL)
    price = models.CharField(max_length=10, blank=True, null=True)


class Story(models.Model):
    user = models.ForeignKey(Customuser, related_name="user_story", null=True, blank=True,
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_story, default='users/default.png')
    title = models.TextField(max_length=300, null=True, blank=True)
    video = models.FileField(upload_to=get_storyved, default='users/default.mp3')
    name = models.CharField(max_length=255, blank=True, null=True)
    views = models.IntegerField(default=0, blank=True, null=True)
    anonymity = models.CharField(max_length=255, null=True, blank=True)
    transparency = models.CharField(max_length=255, null=True, blank=True)
    authenticity = models.CharField(max_length=255, null=True, blank=True)
    bid_buy = models.CharField(max_length=255, null=True, blank=True)
    authenticate = models.CharField(max_length=255, null=True, blank=True)
    prosper = models.CharField(max_length=255, null=True, blank=True)
    ask_sell = models.CharField(max_length=255, null=True, blank=True)
    authenticity1 = models.CharField(max_length=255, null=True, blank=True)
    prosper1 = models.CharField(max_length=255, null=True, blank=True)
    is_image = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Comment(models.Model):
    user = models.ForeignKey(Customuser, related_name="user_com", null=True, blank=True,
                             on_delete=models.CASCADE)
    desc = models.TextField(max_length=255, null=True, blank=True)
    like = models.IntegerField(default=0, null=True, blank=True)
    story = models.ForeignKey('Story', related_name="comment", null=True, blank=True,
                              on_delete=models.CASCADE)

    # product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user)


class Order(models.Model):
    STATUS_CHOICES = (
        ('current', 'Current'),
        ('pending', 'Pending'),
        ('history', 'History')
    )
    user = models.ForeignKey(Customuser, related_name="user_or", null=True, blank=True,
                             on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, null=True, blank=True)
    price = models.CharField(default=0, max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_item",on_delete=models.SET_NULL, null=True,)
    praduct = models.ManyToManyField(Product,related_name='praduc')
    price = models.CharField(default=0, max_length=10, null=True, blank=True)
    size = models.ManyToManyField(Allsize,related_name='allsize')

    def __str__(self):
        return str(self.price)






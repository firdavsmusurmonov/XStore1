from django.contrib import admin
from home.models import *

admin.site.site_header = "My applications"


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ImageInline(admin.TabularInline):
    model = Image


class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'color']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [ImageInline]
    search_fields = ['name']
    filter_horizontal = ['color']


class AllsizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'size']
    # inlines = [ImageInline]
    # search_fields = ['']


class CommentInline(admin.TabularInline):
    model = Comment


class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    inlines = [CommentInline]
    search_fields = ['name']
    # filter_horizontal = ['color']


class InfomationAdmin(admin.ModelAdmin):
    list_display = ['id', 'style']


class ImageAdmin(admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['image']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', "user"]


class ProductPriceAdmin(admin.ModelAdmin):
    list_display = ['id']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'price']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(ProductPrice, ProductPriceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Allsize, AllsizeAdmin)
admin.site.register(Infomation, InfomationAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Comment, CommentAdmin)

from django.contrib import admin
from account.models import *
from  home.models import *


class CustomuserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']


class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Customuser, CustomuserAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Language, LanguageAdmin)

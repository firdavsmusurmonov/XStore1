from rest_framework import serializers
from account.models import *


class CustomuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["id", "username", "smscode"]

class CustomuserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ["id", "username"]


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name"]

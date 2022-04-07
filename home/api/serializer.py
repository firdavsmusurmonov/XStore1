from rest_framework import serializers

from account.api.serializer import *
from home.models import *


class ProductSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    # color = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    # def get_image(self, obj):
    #     image = Image.objects.filter(product=obj).all()
    #     return ImageSerializer(image, many=True, context={'request': self.context['request']}).data
    #
    # def get_color(self, obj):
    #     if obj.color:
    #         return ColorSerializer(obj.color, many=True, context={'request': self.context['request']}).data
    #     return None
    #
    # def get_category(self, obj):
    #     return CategorySerializer(obj.category, many=False, context={'request': self.context['request']}).data


class ProductTSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", 'name', 'color', 'image', 'title', 'desc', 'category']

    def get_image(self, obj):
        image = Image.objects.filter(product=obj).all()
        return ImageSerializer(image, many=True, context={'request': self.context['request']}).data

    def get_color(self, obj):
        if obj.color:
            return ColorSerializer(obj.color, many=True, context={'request': self.context['request']}).data
        return None

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=False, context={'request': self.context['request']}).data


class ProductPriceDetailSerializer:
    pass


class ProductDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'image', 'name', 'brend']

    def get_image(self, obj):
        image = Image.objects.filter(product=obj).first()
        if image:
            return ImageSerializer(image, many=False, context={'request': self.context['request']}).data
        return None

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=False, context={'request': self.context['request']}).data


class StoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ["id", 'name', 'image', 'title', 'anonymity', 'transparency', 'authenticity', 'bid_buy',
                  'authenticate', 'prosper',
                  'ask_sell', 'authenticity1', 'prosper1']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class StoryVideoSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = ["id", 'name', 'user', "views", 'video', 'title', 'comment']

    def get_comment(self, obj):
        comment = Comment.objects.filter(story=obj).all()
        return CommentSerializer(comment, many=True, context={'request': self.context['request']}).data


class ProductPriceSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()

    class Meta:
        model = ProductPrice
        fields = ['id', 'size', 'price']

    def get_size(self, obj):
        return AllsizeSerializer(obj.size, many=False, context={'request': self.context['request']}).data


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_user(self, obj):
        return CustomuserOrderSerializer(obj.user, many=False, context={'request': self.context['request']}).data


class OrderItemSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    praduct = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    #
    def get_size(self, obj):
        return AllsizeSerializer(obj.size, many=True, context={'request': self.context['request']}).data

    def get_praduct(self, obj):
        return ProductSerializer(obj.praduct, many=True, context={'request': self.context['request']}).data


class ProductPriceBidBuySerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = ProductPrice
        fields = ['id', 'size', 'price', 'product']

    def get_size(self, obj):
        return AllsizeSerializer(obj.size, many=False, context={'request': self.context['request']}).data

    def get_product(self, obj):
        return ProductDetailSerializer(obj.product, many=False, context={'request': self.context['request']}).data


class AllsizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allsize
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

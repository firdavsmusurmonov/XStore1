from home.api.serializer import *
# from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from rest_framework import viewsets
from rest_framework import generics, mixins, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from home.api.filters import ProductFilter, AllsizeFilter
# from rest_framework.pagination import LargeResultsSetPagination
from xstore.pagination import LargeResultsSetPagination

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class StoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = instance.views + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'category__name', 'brend']
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action == "list":
            return ProductTSerializer
        else:
            return ProductDetailSerializer


class AllsizeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Allsize.objects.all()
    serializer_class = AllsizeSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['price', 'size']
    # search_fields = ['price']
    filterset_class = AllsizeFilter


class ProductPriceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['price', 'size']
    # search_fields = ['price']
    # filterset_class = AllsizeFilter


class OrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


class OrderItemViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]


#
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def storyimagevideo(request):
    story_id = request.GET.get("story_id")
    story = Story.objects.filter(pk=story_id).first()
    if story.is_image == True:
        result = {
            'status': 1,
            'msg': StoryImageSerializer(story, many=False, context={"request": request}).data
        }
        return Response(result, status=status.HTTP_200_OK)
    elif story.is_image == False:
        result = {
            'status': 1,
            'msg': StoryVideoSerializer(story, many=False, context={"request": request}).data
        }
        return Response(result, status=status.HTTP_200_OK)
    else:
        result = {
            'status': 0,
            'msg': "story not found"
        }
        return Response(result)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def bidbuy(request):
    productprice_id = request.GET.get("productprice_id")
    productprice = ProductPrice.objects.filter(id=productprice_id).first()
    if productprice:
        result = {
            'status': 1,
            'msg': ProductPriceBidBuySerializer(productprice, many=False, context={"request": request}).data
        }
        return Response(result, status=status.HTTP_200_OK)
    else:
        result = {
            'status': 0,
            'msg': "story not found"
        }
        return Response(result)

@api_view(['GET'])
@permission_classes([AllowAny, ])
def myprofil(request):
    user_id = request.GET.get("user_id")
    user = Customuser.objects.filter(id=user_id).first()
    if user:
        result = {
            'status': 1,
            'msg': CustomuserProfilSerializer(user, many=False, context={"request": request}).data
        }
        return Response(result, status=status.HTTP_200_OK)
    else:
        result = {
            'status': 0,
            'msg': "user not found"
        }
        return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def order_status(request):
    try:
        status = request.GET['status']
        if status:
            order = Order.objects.filter(status=status).all()

            result = {
                'status': 1,
                'order': OrderSerializer(order, many=True, context={"request": request}).data
            }
            return Response(result)
        else:
            result = {
                'status': "Order not define",
            }
            return Response(result)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

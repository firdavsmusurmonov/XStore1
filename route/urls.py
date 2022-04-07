from account.api.views import *
from click.api.views import ClickUzMerchantAPIView
from home.api.views import *
from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'region', RegionViewSet)
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'story', StoryViewSet)
router.register(r'allsize', AllsizeViewSet)
router.register(r'productPrice', ProductPriceViewSet)
router.register(r'orderitem', OrderItemViewSet)
router.register(r'order', OrderViewSet)


from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', register),
    path('register-accept', register_accept),
    path('login', login),
    path('forget-password', forget_password),
    path('forget-accept', forget_accept),
    path('storyimagevideo', storyimagevideo),
    path('bidbuy', bidbuy),
    path('click', csrf_exempt(ClickUzMerchantAPIView.as_view())),
]
urlpatterns += router.urls

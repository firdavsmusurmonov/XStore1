import django_filters
from home.models import Product, Allsize


class ProductFilter(django_filters.FilterSet):
    justDropped = django_filters.BooleanFilter(field_name='justDropped')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ["justDropped", 'mostPopular','brend']


class AllsizeFilter(django_filters.FilterSet):
    # justDropped = django_filters.BooleanFilter(field_name='justDropped')
    # name = django_filters.CharFilter(field_name='price', lookup_expr='icontains')

    class Meta:
        model = Allsize
        fields = ["size"]

#
# class NotificationFilter(django_filters.FilterSet):
#     notifation_type = django_filters.ModelChoiceFilter(queryset=NotifationType.objects.all())
#
#     class Meta:
#         model = Notifation
#         fields = ["notifation_type"]
#
# class MessageFilter(django_filters.FilterSet):
#     thread = django_filters.ModelChoiceFilter(queryset=Thread.objects.all())
#
#     class Meta:
#         model = Message
#         fields = ["thread"]

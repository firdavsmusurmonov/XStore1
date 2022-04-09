import random
from unittest import case

from account.api.serializer import *
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_jwt.settings import api_settings
from xstore import settings
from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from ..models import Customuser
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework import generics, mixins, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status, generics, filters
from django_filters.rest_framework import DjangoFilterBackend

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Customuser.objects.all()
    serializer_class = CustomuserSerializer
    # pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['first_name']
    search_fields = ['first_name']


class RegionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    # pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']


class LanguageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    # pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register(request):
    try:
        username = request.data.get('first_name')
        email = request.data.get('email')
        password = request.data.get('password')
        if not login:
            res = {
                'status': 0,
                'msg': 'Login empty',
            }
            return Response(res)

        user = Customuser.objects.filter(first_name=username).first()
        if not user:
            user = Customuser.objects.create(
                first_name=username,
                username=username,
                email=email,
                complete=0
            )
        elif user:
            res = {
                'msg': 'User exits',
                'status': 0,
            }
            return Response(res)
        smscode = random.randint(1000, 9999)
        user.set_password(str(password))
        user.smscode = smscode
        user.email = email
        user.save()
        send_sms(email, "Sizning tasdiqlash codingiz: " + str(smscode))

        if user:
            result = {
                'status': 1,
                'msg': 'Sms sended',
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            res = {
                'status': 0,
                'msg': 'Can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def register_accept(request):
    try:
        sms_code = request.data.get('sms_code')
        username = request.data.get('first_name')
        user = Customuser.objects.filter(first_name=username).first()

        if user and str(user.smscode) == str(sms_code):
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.complete = 1
            user.save()
            result = {
                'status': 1,
                'user': CustomuserSerializer(user, many=False, context={"request": request}).data,
                'token': token
            }
        else:
            result = {
                'status': 0,
                'msg': 'Sms not equal',

            }
        return Response(result)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        if not login:
            res = {
                'msg': 'Login empty',
                'status': 0,
            }
            return Response(res)

        user = Customuser.objects.filter(username=username).first()
        if not user:
            user = Customuser.objects.filter(email=username).first()
            if not user:
                res = {
                    'msg': 'email or password wrond',
                    'status': 0,
                }
                return Response(res)
        print(user)
        if user and user.check_password(str(password)):
            if user.complete == 0:
                res = {
                    'msg': 'email sms code not check',
                    'status': 0,
                }
                return Response(res)
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            result = {
                'status': 1,
                'msg': 'Sms sended',
                'user': CustomuserSerializer(user, many=False, context={"request": request}).data,
                'token': token
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            res = {
                'status': 0,
                'msg': 'Can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)



# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def login(request):
#     try:
#         username = request.data.get('username')
#         password = request.data.get('password')
#         if not login:
#             res = {
#                 'msg': 'Login empty',
#                 'status': 0,
#             }
#             return Response(res)
#
#         user = Customuser.objects.filter(username=username).first()
#         if not user:
#             user = Customuser.objects.filter(email=username).first()
#             if not user:
#                 res = {
#                     'msg': 'email or password wrond',
#                     'status': 0,
#                 }
#                 return Response(res)
#         print(user)
#         if user and user.check_password(str(password)):
#             if user.complete == 0:
#                 res = {
#                     'msg': 'email sms code not check',
#                     'status': 0,
#                 }
#                 return Response(res)
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             result = {
#                 'status': 1,
#                 'msg': 'Sms sended',
#                 'user': CustomuserSerializer(user, many=False, context={"request": request}).data,
#                 'token': token
#             }
#             return Response(result, status=status.HTTP_200_OK)
#         else:
#             res = {
#                 'status': 0,
#                 'msg': 'Can not authenticate with the given credentials or the account has been deactivated'
#             }
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#     except KeyError:
#         res = {
#             'status': 0,
#             'msg': 'Please set all reqiured fields'
#         }
#         return Response(res)
#

from django.core.mail import EmailMessage


def send_sms(mail, text):
    email = EmailMessage('Veri', text, to=[mail])
    email.send()


@api_view(['POST'])
@permission_classes([AllowAny, ])
def forget_password(request):
    try:
        username = request.data.get('email')
        user = Customuser.objects.filter(email=username).first()
        if user:
            smscode = random.randint(1000, 9999)
            user.smscode = smscode
            user.save()
            send_sms(user.email, "Tasdiqlash codi " + str(smscode))
            result = {
                'status': 1,
                'msg': 'Sms send',
                "email": user.email
            }
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {
                'status': 1,
                'msg': 'User not found'
            }
            return Response(result, status=status.HTTP_200_OK)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def forget_accept(request):
    try:
        sms_code = request.data.get('sms_code')
        username = request.data.get('email')
        user = Customuser.objects.filter(email=username).first()
        if user and str(user.smscode) == str(sms_code):
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            user.complete = 1
            # user.set_password(new_password)
            user.save()
            result = {
                'status': 1,
                'user': CustomuserSerializer(user, many=False, context={"request": request}).data,
                'token': token
            }
        else:
            result = {
                'status': 1,
                'msg': 'Sms not equal',

            }
        return Response(result)
    except KeyError:
        res = {
            'status': 0,
            'msg': 'Please set all reqiured fields'
        }
        return Response(res)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated, ])
# def profil(request):
#     try:
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         avatar = request.data.get('avatar')
#         nickname = request.data.get('nickname')
#         email = request.data.get('email')
#         Number = request.data.get('Number')
#         gender = request.data.get('gender')
#         birth_date = request.data.get('birth_date')
#         user = request.user
#         user.first_name = first_name
#         user.avatar = avatar
#         user.email = email
#         user.Number = Number
#         user.nickname = nickname
#         user.last_name = last_name
#         user.gender = gender
#         user.birth_date = birth_date
#         if 'avatar' in request.data:
#             user.avatar = request.data['avatar']
#         user.save()
#
#         result = {
#             'status': 1,
#             'msg': 'User updated',
#             'user': CustomuserAccauntSerializer(user, many=False, context={"request": request}).data
#         }
#         return Response(result, status=status.HTTP_200_OK)
#     except KeyError:
#         res = {
#             'status': 0,
#             'msg': 'Please set all reqiured fields'
#         }
#         return Response(res)
#
# @api_view(['GET'])
# @permission_classes([IsAuthenticated, ])
# def me(request):
#     try:
#         user = request.user
#         result = {
#             'status': 1,
#             'user': CustomuserAccauntSerializer(user, many=False, context={"request": request}).data
#         }
#         return Response(result, status=status.HTTP_200_OK)
#     except KeyError:
#         res = {
#             'status': 0,
#             'msg': 'Please set all reqiured fields'
#         }
#         return Response(res)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated, ])
# def set_password(request):
#     try:
#         old_password = request.data.get('old_password')
#         new_password = request.data.get('new_password')
#         user = request.user
#         if user.check_password(old_password):
#             user.set_password(new_password)
#             user.save()
#             result = {
#                 'status': 1,
#                 'msg': 'User password updated',
#                 'user': CustomuserSerializer(user, many=False, context={"request": request}).data
#             }
#             return Response(result, status=status.HTTP_200_OK)
#         else:
#             result = {
#                 'status': 1,
#                 'msg': 'User old password wrong'
#             }
#             return Response(result, status=status.HTTP_200_OK)
#     except KeyError:
#         res = {
#             'status': 0,
#             'msg': 'Please set all reqiured fields'
#         }
#         return Response(res)
# n = int(input())
# def number(n):
# 	match n:
# 		case 1:
# 			return 6
# 		case 2:
# 			return 5
# 		case 3:
# 			return 4
# 		case 4:
# 			return 3
# 		case 5:
# 			return 2
# 		case 6:
# 			return 1
# print(number(n))


# if __name__ = "__main__":
# 	agrument = 0

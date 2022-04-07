from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from click.models import Transaction
from rest_framework.permissions import AllowAny
from click.click_authorization import click_authorization
from .serializer import ClickUzSerializer
from click.status import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer

class ClickUzMerchantAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    VALIDATE_CLASS = None
    renderer_classes = [JSONRenderer]
    def post(self, request):
        serializer = ClickUzSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        METHODS = {
            PREPARE: self.prepare,
            COMPLETE: self.complete
        }

        merchant_trans_id = serializer.validated_data['merchant_trans_id']
        amount = serializer.validated_data['amount']
        action = serializer.validated_data['action']

        if click_authorization(**serializer.validated_data) is False:
            return Response({
                "error": AUTHORIZATION_FAIL_CODE,
                "error_note": AUTHORIZATION_FAIL
            })


        # order = Order.objects.filter(id=merchant_trans_id).first()
        if merchant_trans_id == "1255550000000000000000555555":
            return Response({
                "error": -5,
                "error_note": AUTHORIZATION_FAIL
            })
        order = True
        if order:
            result = METHODS[action](**serializer.validated_data, response_data=serializer.validated_data)
            return Response(result)
        return Response({"error": "Order not found"})

    def prepare(self, click_trans_id: str, merchant_trans_id: str, amount: str, sign_string: str, sign_time: str,
                response_data: dict,
                *args, **kwargs) -> dict:
        """
        :param click_trans_id:
        :param merchant_trans_id:
        :param amount:
        :param sign_string:
        :param response_data:
        :param args:
        :return:
        """
        transaction = Transaction.objects.create(
            click_trans_id=click_trans_id,
            merchant_trans_id=merchant_trans_id,
            amount=amount,
            action=PREPARE,
            sign_string=sign_string,
            sign_datetime=sign_time,
        )
        response_data.update(merchant_prepare_id=transaction.id)
        return response_data

    def complete(self, click_trans_id, amount, error, merchant_prepare_id,
                 response_data, action, *args, **kwargs):
        """
        :param click_trans_id:
        :param merchant_trans_id:
        :param amount:
        :param sign_string:
        :param error:
        :param merchant_prepare_id:
        :param response_data:
        :param action:
        :param args:
        :return:
        """
        try:
            transaction = Transaction.objects.get(pk=merchant_prepare_id)

            if error == A_LACK_OF_MONEY:
                response_data.update(error=A_LACK_OF_MONEY_CODE)
                transaction.action = A_LACK_OF_MONEY
                transaction.status = Transaction.CANCELED
                transaction.save()
                return response_data

            if transaction.action == A_LACK_OF_MONEY:
                response_data.update(error=A_LACK_OF_MONEY_CODE)
                return response_data

            if transaction.amount != amount:
                response_data.update(error=INVALID_AMOUNT)
                return response_data

            if transaction.action == action:
                response_data.update(error=INVALID_ACTION)
                return response_data

            transaction.action = action
            transaction.status = Transaction.FINISHED
            transaction.save()
            response_data.update(merchant_confirm_id=transaction.id)
            # order = Order.objects.filter(pk=transaction.merchant_trans_id).first()
            # order.status = True
            # order.save()
            return response_data
        except Transaction.DoesNotExist:
            response_data.update(error=TRANSACTION_NOT_FOUND)
            return response_data

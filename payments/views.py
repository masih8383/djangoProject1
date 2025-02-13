import uuid
import requests

from django.utils import timezone
from datetime import timedelta

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from payments.models import Payment, Gateway
from django.shortcuts import render
from .serializers import (GatewaySerializer,PaymentSerializer)
from products.models import Product
from django.http import HttpResponseNotFound


class GatewayView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        geteway =Gateway.objects.filter(is_enable=True)
        serializer = GatewaySerializer(geteway, many=True)
        return Response(serializer.data)



class PaymentView(APIView):
    def get(self, request):
        geteway_id =request.query_params.get('geteway')
        package_id = request.query_params.get('package')

        try:
            package = Gateway.objects.get(pk=package_id, is_enable=True)
            geteway = Gateway.objects.get(pk=geteway_id, is_enable=True)
        except(package.DoesNotExist, Gateway.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(
            user=request.user,
            package=package,
            geteway=geteway,
            price=package.price,
            phone_number=request.user.phone_number,
            token=str(uuid.uuid4()))

        return Response({'token':payment.token, 'callback_url':'https://my-site.com/payments/pay/'})

    def post(self, request):
        token = request.data.get('token')
        st = request.data.get('status')

        try:
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if st !=10:
            payment.status = Payment.STATUS_CANCELED
            payment.save()
            return Response({'detail':'Payment has been canceled'},status=status.HTTP_404_NOT_FOUND)


        r =requests.post('bank_vreify_url ', data={})
        if r.status_code != 200:
            payment.status = Payment.STATUS_ERROR
            payment.save()

            return Response({'detail':'Payment has been canceled'},status=status.HTTP_404_NOT_FOUND)


        payment.status=payment.STATUS_PAID
        payment.save()
        return Response({'detail: payment is ok'})






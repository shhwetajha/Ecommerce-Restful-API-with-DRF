from .import client
from rest_framework import status
from rest_framework.serializers import ValidationError

class RazorPayClient:
    def create_order(self,amount,currency):
        data={'amount':int(amount),'currency':'INR'}
        try:
            order_data=client.order.create(data=data)
            return order_data
        except Exception as e:
            raise ValidationError({'status':status.HTTP_400_BAD_REQUEST,'msg':e})
            
from rest_framework import serializers
from .models import *
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator,default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .views import *
from .utils import *
from djoser.serializers import UserCreateSerializer
from products.serializers import *
from cart.models import *
from django.db import transaction


class RegSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone','password','password2']
        extra_kwargs={'password':{'write_only':True}}

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.pop('password2')
        print('jjjjjjjjjjjjjjjjjjjjjjjj')
        if password != password2:
            raise serializers.ValidationError('password and confirm password do not match')
        return attrs
    
    def create(self,validate_data):     
        user=Account.objects.create(**validate_data)
        user.set_password(validate_data['password'])
        user.save()
        return user
        
class loginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model=Account
        fields=['email','password'] 
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['first_name','last_name','username','email','phone']







class ChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=100,style={'input_type':'password'},write_only=True)
    class Meta:
        model=Account
        fields=['password','password2']

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.pop('password2')
        user=self.context.get('user')

        if password != password2:
            raise serializers.ValidationError('password and confirm_password do not match!')
        user.set_password(password)
        user.save()
        return attrs
    

class ForgotPSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model=Account
        fields=['email']

    def validate(self,attrs):
        email=attrs.get('email')

        
        if Account.objects.filter(email__iexact=email).exists():
            user=Account.objects.get(email=email)

            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:3000/fapp/Forgotpassword/'+uid+'/'+token
            print(link)
            body='Click Following link to reset your password '+link
            data={'subject':'Reset Your Password',
                  'body':body,
                  'to_email':user.email}
            util.send_email(data)
            return attrs
        else:
            serializers.ValidationError('you are not a registered user')

class ForgotPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=100,style={'input_type':'password'},write_only=True)
    
    class Meta:
        model=Account
        fields=['password','password2']

    def validate(self,attrs):
        try: 
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')

            if password!=password2:
                raise serializers.ValidationError('password and password2 does not match')
            id=smart_str(urlsafe_base64_decode(uid))
            user=Account.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Password Reset Link is not valid')
            user.set_password(password)
            user.save() 
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator.check_token(user,token)
            raise serializers.ValidationError('Token is not valid or expired!')


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields=['id','first_name','last_name','email','username','password']


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProfilePicture
        fields=['id','name','bio','profile_picture']

class create_orderserializer(serializers.Serializer):
    cart_id=serializers.UUIDField()

    class Meta:
        model=Orders

    def save(self,**kwargs):
        with transaction.atomic():
            cart_id=self.validated_data['cart_id']
            user_id=self.context['user_id']
            orders=Orders.objects.create(owner_id=user_id)

            cart_items=cart_itemsecond.objects.filter(cart_id=cart_id)
            order_items=[OrderItem(order=orders,product=item.product,quantity=item.quantity)for item in cart_items]
            OrderItem.objects.bulk_create(order_items)
            cartsecond.objects.filter(id=cart_id).delete()

# 34073a01-95b8-4333-9106-b3f6f34dea45

    
        



class OrderItemSerializers(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializers(many=True,read_only=True)
    class Meta:
        model=Orders
        fields=['id','placed_at','payment_status','owner','items']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['first_name','last_name','email']

class UserProfileSerializer(serializers.ModelSerializer):
    user=AccountSerializer(many=False,read_only=True)
    class Meta:
        model=UserProfileModel
        fields=['address_line_1','address_line_2','profile_picture','state','city','country','user']
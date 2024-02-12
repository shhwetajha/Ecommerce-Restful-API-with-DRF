from rest_framework import serializers
from .models import *
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator,default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .views import *
from .utils import *


class RegSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone','password','password2']
        extra_kwargs={'password':{'write_only':True}}

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.pop('password2')
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


       
          

        
            


from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes,smart_str,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.conf import settings
from fapp.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import *

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class Registeration(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=RegSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save() 
            email=serializer.data.get('email') 
            user.username=email.split('@')[0]
            user.phone=serializer.data.get('phone')  
            user.save() 
            reg_token=get_tokens_for_user(user)

            user=Account.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            current_site=get_current_site(request)
            domain=str(current_site)
            token=default_token_generator.make_token(user)
            link='http://'+domain+'/fapp/activation/'+uid+'/'+token
            print(link)
            body="Click on below link to confirm your registeration "+link
            data={'subject':'Account Registeration confirmation',
                  'body':body,
                  'to_email':user.email}
            util.send_email(data)                  
            return Response({'data':['data registered successfully! account confirmation mail has been sent to your email address',reg_token]},status=status.HTTP_201_CREATED)
        else:
            return Response({'error':serializer.error},status=status.HTTP_400_BAD_REQUEST)
        
class activation(APIView):
    renderer_classes=[UserRenderer]
    def get(self,request,uid,token):
        try:
            id=smart_str(urlsafe_base64_decode(uid))
            user=Account.objects.get(id=id)
            if not default_token_generator.check_token(user,token):
                return Response({'error':'link is invalid or expired'},status=status.HTTP_400_BAD_REQUEST)
            user.is_active=True
            user.save()
            return Response({'data':'Your account has been successfully activated!'},status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            default_token_generator.check_token(user,token)
            return Response({'error':'link is invalid or expired'},status=status.HTTP_400_BAD_REQUEST)
               
class view_login(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=loginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'message':'success','token':token},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'non_field_error':"email or password not correct"}},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':serializer.error},status=status.HTTP_400_BAD_REQUEST)
            
class UserProfile(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=UserProfileSerializer(request.user)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    

class UserChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]

    def post(self,request):
        serializer=ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            return Response({'data':'password changed successfully!'},status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.error},status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordmail(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=ForgotPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'data':'an email has been sent to your email address'},status=status.HTTP_200_OK)
        else:
            return Response({'error':[serializer.error,]},status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token):
        serializer=ForgotPasswordSerializer(data=request.data,context={'uid':uid,'token':token,})
        if serializer.is_valid():
            return Response({'data':'password changed successfully!'})
        else:
            return Response({'error':serializer.error},status=status.HTTP_400_BAD_REQUEST)




      
           
        



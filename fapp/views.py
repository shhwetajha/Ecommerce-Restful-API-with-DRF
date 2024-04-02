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
from rest_framework.decorators import api_view,action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.conf import settings
from fapp.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import *
from cart.models import cart_itemsecond
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser,FormParser
from .models import *
import json
from .import client
from .main import RazorPayClient
from rest_framework.mixins import CreateModelMixin,UpdateModelMixin,RetrieveModelMixin
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
rz_client=RazorPayClient()

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
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
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
            print(token)
            link='http://'+domain+'/fapp/activation/'+uid+'/'+token
            print(link)
            body="Click on below link to confirm your registeration "+link
            data={'subject':'Account Registeration confirmation',
                  'body':body,
                  'to_email':user.email}
            util.send_email(data)                  
            return Response({'data':['data registered successfully! account confirmation mail has been sent to your email address',reg_token]},status=status.HTTP_201_CREATED)
        else:
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
class activation(APIView):
    renderer_classes=[UserRenderer]
    def get(self,request,uid,token):
        try:
            uid=smart_str(urlsafe_base64_decode(uid))
            user=Account.objects.get(id=uid)
            if not default_token_generator.check_token(user,token):
                return Response({'error':'link is invalid or expired'},status=status.HTTP_400_BAD_REQUEST)
            user.is_active=True
            user.save()
            return Response({'data':'account has been successfully activated!'},status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            default_token_generator.check_token(user,token)
            return Response({'error':'link is expired or invalid'})    

        
               
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
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
class view_loginn(viewsets.ViewSet):
    def create(self, request, pk=None):
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
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
            
class UserProfile(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=UserProfileSerializer(request.user)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)

# class Userdetail(APIView):
#     renderer_classes=[UserRenderer]
#     permission_classes=[IsAuthenticated]
#     def get(self,request):
#         serializer=UserProfileSerilaizer(request.user)
#         return Response({'data':serializer.data},status=status.HTTP_200_OK)
      
# class Userdetail(APIView):
#     renderer_classes=[UserRenderer]
#     permission_classes=[IsAuthenticated]
#     def get(self,request):
#         serializer=UserProfileSerilaizer(request.user)
#         return Response({'data':serializer.data},status=status.HTTP_200_OK)

class UserChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[UserRenderer]

    def post(self,request):
        serializer=ChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            return Response({'data':'password changed successfully!'},status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordmail(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=ForgotPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'data':'an email has been sent to your email address'},status=status.HTTP_200_OK)
        else:
            return Response({'error':[serializer.errors,]},status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token):
        serializer=ForgotPasswordSerializer(data=request.data,context={'uid':uid,'token':token,})
        if serializer.is_valid():
            return Response({'data':'password changed successfully!'})
        else:
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)





# class activation(APIView):
#     def get(self,request,uid,token):
#         try:
#             uid=smart_str(urlsafe_base64_decode(uid))
#             user=Account.objects.get(id=uid)
#             if not default_token_generator.check_token(user,token):
#                 return Response({'error':'link is invalid or expired'},status=status.HTTP_400_BAD_REQUEST)
#             user.is_active=True
#             user.save()
#             return Response({'data':'account has been successfully activated!'},status=status.HTTP_200_OK)
#         except DjangoUnicodeDecodeError as identifier:
#             default_token_generator.check_token(user,token)
#             return Response({'error':'link is expired or invalid'})    

class profile_picture(ModelViewSet):
    queryset=ProfilePicture.objects.all()
    serializer_class=ProfilePictureSerializer
    parser_classes=(MultiPartParser,FormParser)

    def create(self,request,*args,**kwargs):
        name=request.data.get('name')
        bio=request.data.get('bio')
        profile_picture=request.data.get('profile_picture')

        ProfilePicture.objects.create(name=name,bio=bio,profile_picture=profile_picture)
        return Response('response stored successfully!',status=status.HTTP_200_OK)
    

class view_Orders(ModelViewSet):
    permission_classes=[IsAuthenticated]

    @action(detail=True,methods=['POST'])
    def pay(self,request,pk):
        order=self.get_object()
        amount=order.total_price
        id=order.id
        print(amount)
        currency='INR'
        try:
            order_response=rz_client.create_order(amount=amount,currency=currency)
            print(order_response['id'])
            order=Orders.objects.get(id=id)            
            order.order_payment_id=order_response['id']
            order.save()
            

            response={'status_code':status.HTTP_200_OK,'msg':'order_created','data':order_response}
            return Response(response,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':e,'status':status.HTTP_400_BAD_REQUEST})

    @action(detail=True,methods=['POST'])
    def handle_payment_success(self):
        res=json.loads(request.data['response'])

        raz_order_id=''
        raz_payment_id=''
        raz_signature=''

        for key in res.keys():
            if key=='razorpay_order_id':
                raz_order_id=res[key]
            elif key=='razorpay_payment_id':
                raz_payment_id=res[key]
            elif key=='razorpay_signature':
                raz_signature=res[key]

        data={'razorpay_order_id':raz_order_id,'razorpay_payment_id':raz_payment_id,'razorpay_signature':raz_signature}            
        order=Orders.objects.get(order_payment_id=raz_order_id)

        check=client.utility.verify_payment_signature(data)
        if check is not None:
            order.payment_status='PAYMENT_STATUS_FAILED'
            order.save()
            print('return to error url or error page')
            return Response({'error':'some error occured'})
        else:
            order.payment_status='PAYMENT_STATUS_COMPLETED'
            order.save()
            return Response({'data':'payment_successful'})

    def get_serializer_class(self):
        if self.request.method=='POST':
            return create_orderserializer
        return OrderSerializer
    

    def get_queryset(self):
        user=self.request.user
        if user.is_staff:
            return Orders.objects.all()
        return Orders.objects.filter(owner=user)
    

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
        

# class UserProfileView(ModelViewSet):
#     permission_classes=[IsAuthenticated]
#     queryset=UserProfileModel.objects.all()
#     serializer_class=UserProfileSerializer
#     parser_classes=(MultiPartParser,FormParser)


#     def create(self,request,*args,**kwargs):
#         address_line_1=request.data.get('address_line_1')
#         address_line_2=request.data.get('address_line_2')
#         state=request.data.get('state')
#         city=request.data.get('city')
#         country=request.data.get('country')
#         profile_picture=request.data.get('profile_picture')

#         UserProfileModel.objects.create(user=request.user,address_line_1=address_line_1,address_line_2=address_line_2,state=state,city=city,country=country,profile_picture=profile_picture)
#         return Response('response stored successfully!',status=status.HTTP_200_OK)


    # def get_queryset(self):
    #     user=self.request.user
    #     print(user)
    #     return UserProfileModel.objects.get(user_id=user.id)

    # def get_serializer_class(request):
    #     pass
    #     if self.request.method=='POST':
    #         pass
        
class UserProfileAPiView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=UserProfileModel.objects.get(user=request.user)
        userserializer=UserProfileSerializer(user)
        return Response({'data':userserializer.data},status=status.HTTP_200_OK)

    def patch(self,request):
        user=UserProfileModel.objects.get(user=request.user)
        userserializer=UserProfileSerializer(user,data=request.data,partial=True)
        if userserializer.is_valid():
            userserializer.save()
            return Response({'data':userserializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'error':userserializer.errors},status=status.HTTP_400_BAD_REQUEST)
            



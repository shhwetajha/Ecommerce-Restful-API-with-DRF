from django.shortcuts import render
from rest_framework.views import APIView
from categories.models import *
from django.shortcuts import get_object_or_404
from products.models import *
from products.serializers import * 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from fapp.renderers import UserRenderer
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets 
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend 
from .filters import *
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.viewsets import ModelViewSet

# 'rest_framework.pagination.PageNumberPagination'

# Create your views here.


class categorydetaillist(ListAPIView):
    pagination_classes=[PageNumberPagination]
    queryset=Products.objects.all()
    serializer_class=ProductSerial
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['product_name','description']
    ordering_fields=['created_at']



class categorydetailget(APIView):
    def get(self,request,category_slug=None):
        Categories=get_object_or_404(categories,slug=category_slug)
        product=Products.objects.filter(categories=Categories,is_available=True)
        serializer=ProductSerial(product,many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
      

# product details in modelviewset

class Productdetail(ModelViewSet):
    queryset=Products.objects.all()
    serializer_class=ProductSerial
    
class single_productdet(APIView):
    def get(self,request,category_slug=None,slug=None):
        product_det=Products.objects.get(categories__slug=category_slug,slug=slug)
        serializer=ProductSerializer(product_det)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)

class reviewratingregister(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]

    try:
        def patch(self,request,single_productid):
            Reviewrating=reviewrating.objects.get(user=request.user,product_id=single_productid)
            serializer=Reviewupdateserializer(Reviewrating,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':'review updated successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except reviewrating.DoesNotExist():
        def post(self,request,single_productid):
            product=Products.objects.get(id=single_productid)
            serializer=reviewratingserialzer(data=request.data,context={'user':request.user,'product':product})
            if serializer.is_valid():
                Reviewrating=reviewrating.objects.get(user=request.user)
                Reviewrating.ip=request.META.get('REMOTE_ADDR')
                Reviewrating.save()       
                return Response({'data':'review stored successfully!'},status=status.HTTP_200_OK)
            else:
                return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
            
class search(APIView):
    def get(self,request,keyword=None):
        product_count=0
        if 'keyword' in request.GET:
            keyword=request.GET['keyword']
            product=Products.objects.order_by('created_at').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
            product_count=product.count()
            if product_count != 0:
                serializer=ProductSerial(product,many=True)
                return Response({'data':serializer.data,'product_count':product_count},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'product not found!','product_count':product_count},status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.errors},status=status.HTTP_404_NOT_FOUND)


# reviewrating modelviewset
class ReviewRatingg(ModelViewSet):
    serializer_class=ReviewRatinggSerializer
    

    def get_queryset(self):
        return reviewrating.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return{'product_id':self.kwargs['product_pk']}

    

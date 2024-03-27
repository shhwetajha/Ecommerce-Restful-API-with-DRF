from rest_framework.views import APIView
from products.models import *
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from categories.models import *
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

class home(APIView):
    def get(self,request):
        try:
            product=Products.objects.all()
            serializer=ProductSerializer(product,many=True)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        except:
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class category_type(APIView):
    def get(self,request):
        category=categories.objects.all()
        serializer=categoriesSerializer(category,many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)


class Categorydetail(generics.ListCreateAPIView):     
    queryset=categories.objects.all()
    serializer_class=categoriesSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields=['category_name']

class Categorydetails(generics.RetrieveUpdateDestroyAPIView):
    queryset=categories.objects.all()
    serializer_class=categoriesSerializer

class categoriesdett(ModelViewSet):
    queryset=categories.objects.all()
    serializer_class=categoriesSerializer





            
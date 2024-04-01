from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt 


# Create your views here.

# class Categories(APIView):
#     def get(self,request):
#         category=Categories.objects.all()
#         serializer=CategorySerializer(many=True)

# @api_view(['POST'])
# def Studentget(request):
#     serializer=StudentSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'msg':'data created successfully'},status=status.HTTP_200_OK)
#     return Response({'error':serializer.errors})

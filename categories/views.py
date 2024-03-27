from django.shortcuts import render
from rest_framework import APIView
from .serializers import *

# Create your views here.

class Categories(APIView):
    def get(self,request):
        category=Categories.objects.all()
        serializer=CategorySerializer(many=True)

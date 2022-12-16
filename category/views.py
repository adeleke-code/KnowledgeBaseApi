from django.shortcuts import render
from .serializers import CategorySerializer, TitlesSerializer
from rest_framework import viewsets
from .models import Category, Titles

# Create your views here.

class CategoryView(viewsets.ModelViewSet):
            queryset = Category.objects.all()
            serializer_class = CategorySerializer




class TileView(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer

    




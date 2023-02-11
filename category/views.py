from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, ArticleSerializer
from rest_framework.views import APIView
from account.permissions import IsAdmin
from rest_framework.response import Response
from .models import Category, Articles

# Create your views here.

class CreateCategoryView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data['response'] = 'successfully created a category.'
 
        return Response(data)


class UpdateCategory(APIView):
    permission_classes = (IsAdmin,)
    def put(self, request, pk):
        try:
            instance = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response({'error': 'profile not found'}, status=404)

        serializer = CategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            instance = Category.objects.get(id=pk)
            instance.delete()
            return Response({"message": "post successfully deleted"}, 200)
        except Category.DoesNotExist:
            return Response({"message": "post id does not exist!"}, 404)

class GetCategory(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        data = {
            "all categories": serializer.data
        }
        return Response(data)


class CreateArticleView(APIView):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data['response'] = 'successfully created an article.'
 
        return Response(data)

class UpdateArticleView(APIView):
    permission_classes = (IsAdmin,)

    def put(self, request, pk):
        try:
            instance = Articles.objects.get(id=pk)
        except Articles.DoesNotExist:
            return Response({'error': 'article not found'}, status=404)

        serializer = ArticleSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            instance = Articles.objects.get(id=pk)
            instance.delete()
            return Response({"message": "article successfully deleted"}, 200)
        except Articles.DoesNotExist:
            return Response({"message": "article id does not exist!"}, 404)


class GetArticle(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        all_categories = Articles.objects.all()
        serializer = ArticleSerializer(all_categories, many=True)
        data = {
            "all articles": serializer.data
        }
        return Response(data)
    




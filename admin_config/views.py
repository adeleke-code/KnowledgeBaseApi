from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from . models import AdminPage
from . serializers import AdminSerializer
from account.permissions import IsAdmin

# Create your views here.

class AdminView(APIView):
    serializer_class = AdminSerializer
    permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data['response'] = 'successfully created an admin view.'
 
        return Response(data)

class UpdateAdminView(APIView):
    permission_classes = (IsAdmin,)
    def get(self, request, pk):
        try:
            page_data = AdminPage.objects.get(id=pk)
        except AdminPage.DoesNotExist:
            return Response({"error": "page not found"}, 404)
        serializer = AdminSerializer(page_data)
        data = {
            "page_data": serializer.data
        }
        return Response(data)
    def put(self, request, pk):
        try:
            instance = AdminPage.objects.get(id=pk)
        except AdminPage.DoesNotExist:
            return Response({'error': 'page not found'}, status=404)

        serializer = AdminSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
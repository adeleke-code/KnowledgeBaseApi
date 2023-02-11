from rest_framework import serializers
from . models import AdminPage





class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPage
        fields = [
            'id',
            'text',
            'image'

        ]
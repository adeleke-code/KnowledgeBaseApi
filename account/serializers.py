from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

Admin = User.objects.filter(is_admin=True)

class UserRegistrationSerializer(serializers.ModelSerializer):

	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	class Meta:
		model = User
		fields = ['id', 'name', 'email', 'password', 'password2']
		extra_kwargs = {
				'password': {'write_only': True},
		}	
	def	save(self):
		account = User(
					name=self.validated_data['name'],
					email=self.validated_data['email']
				)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match.'})
		account.set_password(password)
		account.save()

		return account

class AdminRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'password2']
        extra_kwargs = {
				'password': {'write_only': True},
		}	

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password Does not match")
        return attrs
    
    def create(self, validate_data):

        return User.objects.create_admin(**validate_data)
        


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
			'id',
            'email',
            'name'
        ]

    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=700)
    password = serializers.CharField(max_length=700)




class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:

        	return Response({"message": "failed", "error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordSerializer(serializers.Serializer):
    # email = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

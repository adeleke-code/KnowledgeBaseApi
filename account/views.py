from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import UserSerializer, AdminRegistrationSerializer, UserDetailSerializer, LoginSerializer, UserLogoutSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.signals import user_logged_in
from .permissions import IsAdmin
from . generators import generate_password
# Create your views here.

User = get_user_model()


class UserRegisterView(APIView):
    # permission_classes = (IsAdmin,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
                
            password = serializer.validated_data['password'] = generate_password()
            serializer.save()
            
            data = {
                'message' : "success",
                'data' : serializer.data,
                'password': password
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {

                'message' : "failed",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

class AdminRegisterView(APIView):
    def post(self, request):
        serializer = AdminRegistrationSerializer(data=request.data)
        data = {}
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        data['response'] = 'successfully registered a new admin.'
        data['email'] = account.email
        data['name'] = account.name

        return Response(data)

class UserData(APIView):
    # permission_classes = (IsAdmin,)
    def get(self, request, pk):
        try:
            user_data = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, 404)
        serializer = UserDetailSerializer(user_data)
        data = {
            "user_data": serializer.data
        }
        return Response(data)
    def put(self, request, pk):
        try:
            instance = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'user not found'}, status=404)

        serializer = UserDetailSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    def delete(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, 404)
        if user.is_staff == True:
            try:
                user.is_staff = False
            except User.DoesNotExist:
                return Response({"error": "user not found"}, 404)
        else:
            return Response({"error": "user is not a staff"}, 404)
        user.save()
        return Response({"message": "user successfully deactivated"}, 200)




class AllUsersView(ListAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class AllAdminUsersView(ListAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.filter(is_admin=True)
    serializer_class = UserDetailSerializer



class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, email = serializer.validated_data['email'], password = serializer.validated_data['password'])
        if user.is_staff:
            if user.is_admin:
                try:
                    refresh = RefreshToken.for_user(user)
                    user_details = {}
                    user_details['email'] = user.email
                    user_details['access_token'] = str(refresh.access_token)
                    user_details['refresh_token'] = str(refresh)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    data = {
                        'message' : "Admin Login successful",
                        'data' : user_details,
                    }
                    return Response(data, status=status.HTTP_200_OK)
                except Exception as e:
                    raise e
            else:
                try:
                    refresh = RefreshToken.for_user(user)
                    user_details = {}
                    user_details['email'] = user.email
                    user_details['access_token'] = str(refresh.access_token)
                    user_details['refresh_token'] = str(refresh)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    data = {
                        'message' : "User Login successful",
                        'data' : user_details,
                    }
                    return Response(data, status=status.HTTP_200_OK)
                except Exception as e:
                    raise e
        else:
            data = {
                'message'  : "failed",
                'errors': 'The account is not active'
                }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

class ChangePasswordView(generics.GenericAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self):
            obj = self.request.user
            return obj

        def post(self, request):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                data = {
                    'status': 'success',
                    'message': 'Password updated successfully',
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LogoutView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"Status": "Successfully logged out!"}, status=status.HTTP_204_NO_CONTENT)

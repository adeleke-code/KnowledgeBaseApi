from django.urls import path, include
from .views import UserRegisterView, AdminRegisterView, AllUsersView, UserLoginView, LogoutView, ChangePasswordView, AllAdminUsersView, AdminLoginView
from rest_framework_simplejwt.views import TokenRefreshView


    




urlpatterns = [
    path('register/user', UserRegisterView.as_view()),
    path('register/admin', AdminRegisterView.as_view()),
    path('all_admin', AllAdminUsersView.as_view()),
    path('all_users', AllUsersView.as_view()),
    path('user/login', UserLoginView.as_view()),
    path('admin/login', AdminLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('password', ChangePasswordView.as_view()),
    path('refresh', TokenRefreshView().as_view(), name="refresh_token"),
    path('auth/', include('djoser.urls')),




    
    
]

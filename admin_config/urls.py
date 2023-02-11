from django.urls import path, include
from . import views


urlpatterns = [
    path('create', views.AdminView.as_view()),
    path('update/<int:pk>', views.UpdateAdminView.as_view())
    
]

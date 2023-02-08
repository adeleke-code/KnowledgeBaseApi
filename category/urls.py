from django.urls import path, include
from .views import CategoryView, TitleView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'list', CategoryView)
router.register(r'title', TitleView)

urlpatterns = [
    path('/', include(router.urls))
]
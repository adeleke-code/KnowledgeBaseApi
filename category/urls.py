from django.urls import path, include
from .views import CategoryView, TileView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'list', CategoryView)
router.register(r'tile', TileView)

urlpatterns = [
    path('/', include(router.urls))
]
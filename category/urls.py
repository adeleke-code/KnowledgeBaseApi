from django.urls import path, include
from . import views


urlpatterns = [
    path('create', views.CreateCategoryView.as_view()),
    path('update/<int:pk>', views.UpdateCategory.as_view()),
    path('get', views.GetCategory.as_view()),
    path('article', views.CreateArticleView.as_view()),
    path('article/update/<int:pk>', views.UpdateArticleView.as_view()),
    path('article/get', views.GetArticle.as_view())

]

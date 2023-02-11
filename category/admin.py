from django.contrib import admin
from .models import Category, Articles

# Register your models here.
admin.site.register(Category)
class ArticleAdmin(admin.ModelAdmin):
    search_fields = [
        'title'
    ]
admin.site.register(Articles, ArticleAdmin)

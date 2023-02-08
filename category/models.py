from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Articles(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False , blank=False)
    data_glossary = models.URLField(null=False, blank=False)
    play_book = models.URLField(null=False, blank=True)
    time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
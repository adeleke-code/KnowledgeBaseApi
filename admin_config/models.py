from django.db import models

# Create your models here.

class AdminPage(models.Model):
    text = models.CharField(max_length=350, blank=False)
    image = models.ImageField(upload_to='KB_Admin', blank=False)
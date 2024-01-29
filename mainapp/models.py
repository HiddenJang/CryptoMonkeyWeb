from django.db import models

# Create your models here.

class App_mainpage_states(models.Model):

    widget = models.CharField(max_length=120)
    elementType = models.CharField(max_length=120)
    elementValue = models.CharField(max_length=50)
    #author = models.ForeignKey("Author", on_delete=models.CASCADE)
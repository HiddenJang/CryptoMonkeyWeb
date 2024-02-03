from django.db import models

# Create your models here.

class App_mainpage_states(models.Model):

    widget = models.CharField(max_length=30)
    elementType = models.CharField(max_length=30)
    elementName = models.CharField(max_length=30, blank=True)
    elementValue = models.CharField(max_length=30)
    #author = models.ForeignKey("Author", on_delete=models.CASCADE)
from django.db import models

# Create your models here.

class App_mainpage_states(models.Model):

    elementName = models.CharField(max_length=100, blank=True)
    elementValue = models.CharField(max_length=100)
    #author = models.ForeignKey("Author", on_delete=models.CASCADE)

from django.db import models

# Create your models here.

class App_mainpage_states(models.Model):

    elementName = models.CharField(max_length=100, blank=True)
    elementValue = models.CharField(max_length=100)
    #author = models.ForeignKey("Author", on_delete=models.CASCADE)

    @staticmethod
    def add_widgets_states(request) -> None:
        """Внесение состояний элементов (виджетов) главного окна в БД"""

        mainpage_data = dict(request.POST)
        mainpage_data.pop('csrfmiddlewaretoken', 'key not found')
        for data in mainpage_data:
            if App_mainpage_states.objects.filter(elementName=data).exists():
                elementsState = App_mainpage_states.objects.filter(elementName=data).first()
                elementsState.elementValue = mainpage_data[data][0]
            else:
                elementsState = App_mainpage_states()
                elementsState.elementName = data
                elementsState.elementValue = mainpage_data[data][0]
            elementsState.save()

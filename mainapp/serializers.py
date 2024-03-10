from rest_framework import serializers

from .models import App_mainpage_states


class MainpageStatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = App_mainpage_states
        fields = '__all__'
        #fields = ['id', 'widget', 'elementType', 'elementValue']
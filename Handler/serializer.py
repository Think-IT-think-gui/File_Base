from rest_framework import serializers
from . models import *




class Passport_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pass_Port
        fields = '__all__'

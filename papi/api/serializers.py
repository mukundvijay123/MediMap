from rest_framework import serializers
from .models import Accident,Patient,Hospital

#Serializer for Accident

class AccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = ['accident_latitude', 'accident_longitude', 'accident_details']
    

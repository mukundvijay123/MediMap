from rest_framework import serializers
from django import forms
from .models import Accident,Patient,Hospital,Insurance

#Serializer for Accident

class AccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = ['accident_latitude', 'accident_longitude', 'accident_details']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'patient_name', 'gender', 'blood_group', 'contact', 'insurance']
        # No need to add hospital and accident since they will be handled by the backend automatically.
    
    # Optional fields (ensure they are not required)
    patient_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=False, allow_blank=True, default=None)
    blood_group = serializers.CharField(required=False, allow_blank=True, default=None)
    contact = serializers.CharField(required=False, allow_blank=True, default=None)
    insurance = serializers.PrimaryKeyRelatedField(queryset=Insurance.objects.all(), required=False, allow_null=True)



class PatientSummarySerializer(serializers.ModelSerializer):
    # Nested AccidentSerializer to get the associated accident details
    accident = AccidentSerializer(read_only=True)  # This will serialize the related accident details
    
    class Meta:
        model = Patient
        fields = '__all__' 




class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = ['id', 'company_name', 'cover', 'addr', 'email', 'website_url']

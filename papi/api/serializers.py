from rest_framework import serializers
from .models import Hospital, Resource, Insurance, Patient, Accident

# Serializer for the Hospital model
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

# Serializer for the Resource model
class ResourceSerializer(serializers.ModelSerializer):
    hospital = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())

    class Meta:
        model = Resource
        fields = '__all__'

# Serializer for the Insurance model
class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'

class AccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accident
        fields = ['latitude', 'longitude', 'accident_details']

class PatientSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField to represent foreign keys
    hospital = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())
    insurance = serializers.PrimaryKeyRelatedField(queryset=Insurance.objects.all())
    accident = AccidentSerializer()

    class Meta:
        model = Patient
        fields = ['name', 'gender', 'contact', 'hospital', 'insurance', 'accident']

    def create(self, validated_data):
        # Extract accident data from validated data
        accident_data = validated_data.pop('accident')
        
        # Create patient instance
        patient = Patient.objects.create(**validated_data)

        # Create accident and link it to the newly created patient
        Accident.objects.create(patient=patient, **accident_data)

        return patient
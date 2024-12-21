from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Hospital
from .serializers import HospitalSerializer,ResourceSerializer,InsuranceSerializer,PatientSerializer



# Create your views here.
def home(request):
    return render(request,'home.html',{})


@api_view(['POST'])
def add_hospital(request):
    if request.method == 'POST':
        # Create a HospitalSerializer instance with the request data
        serializer = HospitalSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the new hospital to the database
            serializer.save()
            # Return a success response with the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return errors if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def add_resource(request):
    if request.method == 'POST':
        # Create a ResourceSerializer instance with the request data
        serializer = ResourceSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the new resource to the database
            serializer.save()
            # Return a success response with the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return errors if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def add_insurance(request):
    if request.method == 'POST':
        # Create an instance of the InsuranceSerializer with the data from the request
        serializer = InsuranceSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the insurance record to the database
            serializer.save()
            # Return a success response with the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If the data is not valid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def add_patient(request):
    if request.method == 'POST':
        # Create a PatientSerializer instance with the data from the request
        serializer = PatientSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            # Save the patient and related accident to the database
            serializer.save()
            # Return a success response with the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If the data is not valid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
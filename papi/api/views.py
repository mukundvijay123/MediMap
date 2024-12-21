from django.shortcuts import render
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Hospital
from .serializers import HospitalSerializer,ResourceSerializer,InsuranceSerializer,PatientSerializer
from .api_utils import haversine_distance



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
    




@api_view(['GET'])
def get_closest_hospital(request):
    # Extract latitude and longitude from query parameters
    try:
        accident_lat = float(request.GET.get('latitude'))
        accident_lon = float(request.GET.get('longitude'))
    except (TypeError, ValueError):
        return Response({"error": "Invalid latitude or longitude"}, status=400)

    try:
        # Connect to the database
        cursor = connection.cursor()

        # Fetch all hospital locations
        query = """
        SELECT id, hospital_name, latitude, longitude
        FROM API_HOSPITAL
        """
        cursor.execute(query)
        hospitals = cursor.fetchall()
        #print(hospitals)
        closest_hospital = None
        min_distance = float('inf')

        # Iterate over hospitals and calculate the distance
        for hospital in hospitals:
            hospital_id, hospital_name, hospital_lat, hospital_lon = hospital

            # Convert Decimal to float
            hospital_lat = float(hospital_lat)
            hospital_lon = float(hospital_lon)

            # Calculate haversine distance
            distance = haversine_distance(accident_lat, accident_lon, hospital_lat, hospital_lon)

            if distance < min_distance:
                min_distance = distance
                closest_hospital = {
                    'id': hospital_id,
                    'name': hospital_name,
                    'latitude': hospital_lat,
                    'longitude': hospital_lon,
                    'distance': min_distance
                }

        if closest_hospital:
            return Response({
                'id': closest_hospital['id'],
                'name': closest_hospital['name'],
                'latitude': closest_hospital['latitude'],
                'longitude': closest_hospital['longitude'],
                'distance': f"{closest_hospital['distance']:.2f} km"
            })

        return Response({"error": "No hospitals found."}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

    finally:
        cursor.close()
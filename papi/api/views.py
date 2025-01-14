from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Accident
from .serializers import AccidentSerializer
from django.db import connection
from .apiUtils import closestHospital,predict_department


# Create your views here.
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Accident, Patient,Hospital
from .serializers import AccidentSerializer
from .apiUtils import predict_department, closestHospital 


class getBestHospital(APIView):
    def get(self, request):
        serializer = AccidentSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Start the transaction
                with transaction.atomic():
                    # Save the validated Accident data into the database
                    accident = serializer.save()

                    # Extract the accident details from the request
                    accident_description = request.data.get("accident_details", {}).get("description", "")
                    lon = request.data.get("accident_longitude")
                    lat = request.data.get("accident_latitude")

                    # Predict the department based on the accident details
                    predictedDept = predict_department(accident_description)

                    # Finding the closest hospital based on latitude and longitude
                    bestHospital = closestHospital(connection, lat, lon)
                    hospital_id = bestHospital["id"]
                    # Fetch the Hospital instance using hospital_id
                    hospital_instance = Hospital.objects.get(id=hospital_id)

                    # Create the Patient record
                    patient_data = {
                        'hospital': hospital_instance,  # Pass the Hospital instance instead of hospital_id
                        'accident': accident,  # Link to the created Accident
                        'patient_name': request.data.get('patient_name'),
                        'gender': request.data.get('gender'),
                        'blood_group': request.data.get('blood_group'),
                        'contact': request.data.get('contact'),
                    }

                    # Create the Patient object and save it to the database
                    patient = Patient.objects.create(**patient_data)

                    # Return a response indicating the patient and accident were successfully created
                    return Response({
                        'message': 'Patient and Accident created successfully',
                        'patient_id': patient.id,
                        'accident_id': accident.id,
                        'hospital': bestHospital,  
                        'department': predictedDept[0],
                    }, status=status.HTTP_201_CREATED)

            except Exception as e:
                # If an error occurs, the transaction will be rolled back
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            # If the Accident serializer is not valid, return errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
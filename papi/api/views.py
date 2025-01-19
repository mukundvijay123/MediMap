from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Accident, Patient,Hospital
from .serializers import AccidentSerializer,PatientSerializer  
from django.db import connection
from .apiUtils import predict_department, closestHospital 
from django.shortcuts import render, get_object_or_404



class Register(APIView):
    def get(self, request):
        # Rendering the index.html template on GET request
        return render(request, 'index.html')
    


class RegisterPatient(APIView):
    def get(self, request, patient_id):
        # Get patient details using the patient_id from the URL
        patient = get_object_or_404(Patient, id=patient_id)

        # Render the registration template with the patient details
        return render(request, 'registration.html', {'patient': patient})
    
class DashboardLogin(APIView):
    def get(self,request):
        return render(request,'hospital.html')

class getBestHospital(APIView):
    def post(self, request):
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
                    bestHospital = closestHospital(connection, lat, lon,predictedDept[0])
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
        


class CompletePatientRegistrationView(APIView):
    def patch(self, request, pk, format=None):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        # Deserialize and validate the data
        serializer = PatientSerializer(patient, data=request.data, partial=True)  # partial=True allows updating only provided fields
        if serializer.is_valid():
            # Optionally assign hospital and accident from session or request context
            hospital_id = request.session.get('hospital_id')  # Or some other way to fetch hospital
            accident_id = request.session.get('accident_id')  # Or some other way to fetch accident

            if hospital_id and accident_id:
                try:
                    hospital = Hospital.objects.get(id=hospital_id)
                    accident = Accident.objects.get(id=accident_id)
                    patient.hospital = hospital
                    patient.accident = accident
                except (Hospital.DoesNotExist, Accident.DoesNotExist):
                    return Response({"detail": "Hospital or Accident not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Save the updated patient instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

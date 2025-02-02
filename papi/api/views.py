from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Accident, Patient,Hospital
from .serializers import AccidentSerializer,PatientSerializer,PatientSummarySerializer
from django.db import connection
from .apiUtils import predict_department, closestHospital ,get_registered,get_unregistered,getHospitalName
from django.shortcuts import render, get_object_or_404
import logging
from rest_framework.exceptions import NotFound



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
    
class DashboardView(APIView):
    def get(self,request,hospital_id):
        unreg=get_unregistered(hospital_id,connection)
        reg=get_registered(hospital_id,connection)
        context = {
            'registered_patients': reg,
            'unregistered_patients': unreg
        }

        return render(request,'dashboard.html',context)
    


class PatientSummary(APIView):
    def get(self, request, patient_id):
        try:
            # Fetch the patient by the given patient_id
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            # If patient does not exist, return a 404 error
            raise NotFound(detail="Patient not found", code=status.HTTP_404_NOT_FOUND)

        # Serialize the patient along with the associated accident data
        serializer = PatientSummarySerializer(patient)
        
        # Return the serialized data in the response
        return Response(serializer.data)
    


class DashboardDetails(APIView):
    def get(self, request, hospital_id):
        try:
            # Get the hospital name and patient data
            hospital_name = getHospitalName(hospital_id, connection)
            unreg = get_unregistered(hospital_id, connection)
            reg = get_registered(hospital_id, connection)

            # Create the context
            context = { 
                'hospital_name': hospital_name,
                'registered_patients': reg,
                'unregistered_patients': unreg
            }

            # Return the response with status code 200 (OK)
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the error for debugging purposes
            logging.error(f"Error fetching data for hospital_id {hospital_id}: {str(e)}")
            
            # Return an error response with a 500 status code (Internal Server Error)
            return Response(
                {"error": "Something went wrong while fetching hospital details."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class PatientDetails(APIView):
    def get(self, request, patient_id):
        try:
            # Fetch the patient by the provided ID
            patient = Patient.objects.get(id=patient_id)
            
            # Serialize the patient data using the PatientSerializer
            serializer = PatientSerializer(patient)
            
            # Return the serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            # Return error message if the patient doesn't exist
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        


class PatienSummary(APIView):
    def get(self,patient_id):
        patient = Patient.objects.get(id=patient_id)

        return Response()
    

class DischargePatient(APIView):



    def delete(self, request, patient_id):

        try:
            # Start a database transaction to ensure atomicity
            with transaction.atomic():
                # Find the patient by patient_id or return a 404 error if not found
                patient = get_object_or_404(Patient, id=patient_id)

                # Check if the patient already has an associated accident
                accident = patient.accident
                
                if accident:
                    # If there's an associated accident, delete the accident
                    accident.delete()
                
                # Optionally mark the patient as discharged instead of deletion (if desired)
                # We can either update a `discharged` field or just delete the patient record.
                patient.delete()  # This will completely remove the patient record from the database

                return Response({"message": "Patient discharged and associated accident deleted successfully."},
                                status=status.HTTP_200_OK)

        except Exception as e:
            # Handle errors and return a failure response
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


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

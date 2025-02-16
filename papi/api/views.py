from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Accident, Patient,Hospital,Insurance
from .serializers import AccidentSerializer,PatientSerializer,PatientSummarySerializer,InsuranceSerializer
from django.db import connection
from .apiUtils import predict_department, closestHospital ,get_registered,get_unregistered,getHospitalName
from django.shortcuts import render, get_object_or_404
import logging
from rest_framework.exceptions import NotFound
import json



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

        # Serialize patient details
        patient_serializer = PatientSummarySerializer(patient)

        # If patient has insurance, serialize the insurance details
        insurance_data = InsuranceSerializer(patient.insurance).data if patient.insurance else None

        # Construct response
        response_data = {
            "patient": patient_serializer.data,
            "insurance": insurance_data  # Will be None if no insurance exists
        }

        return Response(response_data, status=status.HTTP_200_OK)



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
        


class InsuranceView(APIView):

    def get(self, request, pk=None):
        """Fetch all insurances or a single insurance by ID"""
        if pk:
            try:
                insurance = Insurance.objects.get(pk=pk)
                serializer = InsuranceSerializer(insurance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Insurance.DoesNotExist:
                return Response({"error": "Insurance not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            insurances = Insurance.objects.all()
            serializer = InsuranceSerializer(insurances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new insurance record"""
        serializer = InsuranceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update an existing insurance record"""
        try:
            insurance = Insurance.objects.get(pk=pk)
        except Insurance.DoesNotExist:
            return Response({"error": "Insurance not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InsuranceSerializer(insurance, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompletePatientRegistrationView(APIView):
    def patch(self, request, pk, format=None):
        try:
            patient = Patient.objects.get(pk=pk)
        except Patient.DoesNotExist:
            return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        print("Request Body:", request.body.decode("utf-8"))  # Debugging request body

        # Deserialize and validate the data
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            # First, save validated serializer data to update other fields
            serializer.save()

            # Retrieve hospital and accident from session
            hospital_id = request.session.get("hospital_id")
            accident_id = request.session.get("accident_id")

            if hospital_id:
                try:
                    patient.hospital = Hospital.objects.get(id=hospital_id)
                except Hospital.DoesNotExist:
                    return Response({"detail": "Hospital not found."}, status=status.HTTP_400_BAD_REQUEST)

            if accident_id:
                try:
                    patient.accident = Accident.objects.get(id=accident_id)
                except Accident.DoesNotExist:
                    return Response({"detail": "Accident not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Handle insurance assignment
            insurance_data = request.data.get("insurance", None)
            if insurance_data:
                if isinstance(insurance_data, int):  
                    # Assign existing insurance by ID
                    try:
                        patient.insurance = Insurance.objects.get(id=insurance_data)
                    except Insurance.DoesNotExist:
                        return Response({"detail": "Insurance not found."}, status=status.HTTP_400_BAD_REQUEST)
                elif isinstance(insurance_data, dict):
                    # Create new insurance entry if details are provided
                    company_name = insurance_data.get("company_name")
                    cover = insurance_data.get("cover")
                    addr = insurance_data.get("addr", "")
                    email = insurance_data.get("email", "")
                    website_url = insurance_data.get("website_url", "")

                    if not company_name or cover is None:
                        return Response({"detail": "Insurance company name and cover are required."}, status=status.HTTP_400_BAD_REQUEST)

                    insurance, created = Insurance.objects.get_or_create(
                        company_name=company_name,
                        cover=cover,
                        defaults={"addr": addr, "email": email, "website_url": website_url}
                    )
                    patient.insurance = insurance  # Assign the newly created insurance to the patient

            # Finally, save the updated patient instance
            patient.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
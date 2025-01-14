from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Accident
from .serializers import AccidentSerializer
from django.db import connection
from .apiUtils import closestHospital,predict_department


# Create your views here.
class getBestHospital(APIView):
    def get(self,request):
        serializer = AccidentSerializer(data=request.data)
        

        if serializer.is_valid():
            # Save the validated data into the database
            serializer.save()
            accident_description=request.data.get("accident_details")["description"]
            lon=request.data.get("accident_longitude")
            lat=request.data.get("accident_latitude")
            predictedDept=predict_department(accident_description)

            #finding closest hospital
            bestHospital=closestHospital(connection,lat,lon)
            bestHospital["dept"]=predictedDept[0]

            return Response(bestHospital, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




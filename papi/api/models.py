from django.db import models

# Create your models here.


class Hospital(models.Model):
    id = models.AutoField(primary_key=True) 
    hospital_name = models.CharField(max_length=64)
    latitude = models.FloatField()
    longitude = models.FloatField()
    addr = models.CharField(max_length=128)
    city = models.CharField(max_length=32)
    state_name = models.CharField(max_length=32)
    pincode = models.IntegerField()
    contact = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.hospital_name

class Resource(models.Model):
    id = models.AutoField(primary_key=True) 
    dept = models.CharField(max_length=64)  # Department (max length 64 characters)
    resource_type = models.CharField(max_length=64)  # Type of resource (max length 64 characters)

    def __str__(self):
        return f"{self.dept} - {self.resource_type}"  # String representation of the resource

class Insurance(models.Model):
    id =models.AutoField(primary_key=True)
    company_name=models.CharField(max_length=32,null=True)
    cover=models.IntegerField()
    addr=models.CharField(max_length=64,null=True)
    email=models.CharField(max_length=64, null=True)
    website_url=models.CharField(max_length=64,null=True)

    def __str__(self):
        return self.company_name

class Accident(models.Model):
    id = models.AutoField(primary_key=True)
    date=models.DateTimeField(auto_now_add=True)
    accident_latitude = models.FloatField()
    accident_longitude = models.FloatField()
    accident_details = models.JSONField()

    def __str__(self):
        return f"Accident {self.id}"


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='patients',null=True)
    insurance = models.ForeignKey(Insurance, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients')
    accident = models.ForeignKey(Accident, on_delete=models.CASCADE, related_name='patients')
    patient_name = models.CharField(max_length=64,null=True)
    gender = models.CharField(max_length=16, null=True, blank=True)
    blood_group = models.CharField(max_length=8,null=True)
    contact = models.CharField(max_length=16,null=True)

    def __str__(self):
        return f"{self.patient_name} - {self.hospital.hospital_name}"


class ConsistsOf(models.Model):
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    total_quantity = models.IntegerField(default=0)
    total_available_quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('hospital', 'resource')  # Makes the combination of hospital and resource unique


    def __str__(self):
        return f"{self.hospital.name} - {self.resource.resource_type}"



class Allocated(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='allocated_resources')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allocated_resources')
    quantity_allocated = models.IntegerField()

    def __str__(self):
        return f"Resource {self.resource.resource_type} allocated to {self.patient.patient_name} (Quantity: {self.quantity_allocated})"

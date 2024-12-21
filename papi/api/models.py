from django.db import models

# Create your models here.
class Hospital(models.Model):
    hospital_name = models.CharField(max_length=32)
    addr = models.CharField(max_length=128)
    city = models.CharField(max_length=32)
    state_name = models.CharField(max_length=32)
    pincode = models.IntegerField()
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    contact = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.hospital_name
    

class Resource(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    dept = models.CharField(max_length=32)
    resource_type = models.CharField(max_length=32, null=True, blank=True)
    quantity = models.IntegerField()
    occupied_quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.dept} - {self.resource_type}"

class Insurance(models.Model):
    provider_name = models.CharField(max_length=32, unique=True)
    cover = models.IntegerField()

    def __str__(self):
        return self.provider_name


class Patient(models.Model):
    name = models.CharField(max_length=64)
    gender = models.CharField(max_length=16)
    contact = models.CharField(max_length=12, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, null=True, blank=True, on_delete=models.SET_NULL)
    insurance = models.ForeignKey(Insurance, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Accident(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="accident")  # Use related_name to access accident
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    accident_details = models.JSONField()

    def __str__(self):
        return f"Accident details for {self.patient.name}"
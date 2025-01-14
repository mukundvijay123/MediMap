from django.contrib import admin
from django.db import models
from .models import Hospital,Resource,Patient,Accident,Insurance,ConsistsOf,Allocated

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Resource)
admin.site.register(Patient)
admin.site.register(Accident)
admin.site.register(Insurance)
admin.site.register(ConsistsOf)
admin.site.register(Allocated)
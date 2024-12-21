from django.contrib import admin

# Register your models here.
from .models import Hospital,Resource,Insurance,Patient,Accident

admin.site.register(Hospital)
admin.site.register(Patient)
admin.site.register(Accident)
admin.site.register(Resource)
admin.site.register(Insurance)
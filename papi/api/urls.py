from django.urls import path 
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('api/hospitals/',views.add_hospital, name='add-hospital'),
    path('api/resources/', views.add_resource, name='add-resource'),
    path('api/insurances/', views.add_insurance, name='add-insurance'),
    path('api/patients/', views.add_patient, name='add-patient'),

]
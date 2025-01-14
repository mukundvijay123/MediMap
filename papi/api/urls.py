from django.urls import path 
from . import views
urlpatterns=[
    path('getHospital',views.getBestHospital.as_view(),name='get-hospital'),
    

]
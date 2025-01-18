from django.urls import path 
from . import views
urlpatterns=[
    path('getHospital',views.getBestHospital.as_view(),name='get-hospital'),
    path('register',views.Register.as_view(),name='register')

]
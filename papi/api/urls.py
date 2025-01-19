from django.urls import path 
from . import views
urlpatterns=[
    path('getHospital',views.getBestHospital.as_view(),name='get-hospital'),
    path('register',views.Register.as_view(),name='register'),
    path('api/patient/<int:pk>/complete_registration/', views.CompletePatientRegistrationView.as_view(), name='complete_patient_registration'),
    path('patient/register/<int:patient_id>/', views.RegisterPatient.as_view(), name='register_patient'),
    path('dashboardLogin',views.DashboardLogin.as_view(),name='hosptal_dashboard_login')
]
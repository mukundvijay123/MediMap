from django.urls import path 
from . import views
urlpatterns=[
    path('getHospital',views.getBestHospital.as_view(),name='get-hospital'),
    path('register',views.Register.as_view(),name='register'),
    path('api/patient/<int:pk>/complete_registration/', views.CompletePatientRegistrationView.as_view(), name='complete_patient_registration'),
    path('patient/register/<int:patient_id>/', views.RegisterPatient.as_view(), name='register_patient'),
    path('dashboardLogin',views.DashboardLogin.as_view(),name='hosptal_dashboard_login'),
    path('hospital/dashboard/<int:hospital_id>/', views.DashboardView.as_view(), name='dashboard'),
    path('patients/<int:patient_id>/discharge/', views.DischargePatient.as_view(), name='discharge-patient'),
    path("hospital/getDashboardInfo/<int:hospital_id>/",views.DashboardDetails.as_view(),name='hospital-info'),
    path("patients/details/<int:patient_id>",views.PatientDetails.as_view(),name='patient-info'),
    path("patients/summary/<int:patient_id>",views.PatientSummary.as_view(),name='patiet-summanry'),
    path('insurance/', views.InsuranceView.as_view(),name='insurance'),          
    path('insurance/<int:pk>/', views.InsuranceView.as_view(),name='update_insurances'),
]
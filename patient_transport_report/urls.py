from .views import ListDiagnosisView
from django.urls import path

urlpatterns = [
    path('list_diagnoses/', ListDiagnosisView.as_view(), name='list_diagnoses'),
]
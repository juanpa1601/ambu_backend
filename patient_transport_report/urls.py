from django.urls import path
from .views import (
    ListDiagnosisView,
    ListIPSView,
    ListBuzonView
)

urlpatterns = [
    path('list_diagnoses/', ListDiagnosisView.as_view(), name='list_diagnoses'),
    path('list_ips/', ListIPSView.as_view(), name='list_ips'),
    path('list_buzon/', ListBuzonView.as_view(), name='list_buzon'),
]
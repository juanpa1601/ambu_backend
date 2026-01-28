from django.urls import path
from .views import (
    ListDiagnosisView,
    ListIPSView,
    ListBuzonView,
    GetDetailsReportView,
    SaveReportView,
    ListHemodynamicStatusView,
    ListSkinConditionView,
    ListReportsView,
    GetDetailPatientView
)

urlpatterns = [
    path('list_diagnoses/', ListDiagnosisView.as_view(), name='list_diagnoses'),
    path('list_ips/', ListIPSView.as_view(), name='list_ips'),
    path('list_buzon/', ListBuzonView.as_view(), name='list_buzon'),
    path('<int:report_id>/get_detail_report/', GetDetailsReportView.as_view(), name='get_detail_report'),
    path('report_save/', SaveReportView.as_view(), name='save_report'),
    path('list_hemodynamic_statuses/', ListHemodynamicStatusView.as_view(), name='list_hemodynamic_statuses'),
    path('list_skin_conditions/', ListSkinConditionView.as_view(), name='list_skin_conditions'),
    path('list_reports/', ListReportsView.as_view(), name='list_reports'),
    path('<str:identification_number>/patient/', GetDetailPatientView.as_view(), name='get_detail_patient'),
]
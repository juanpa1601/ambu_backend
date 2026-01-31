from typing import Any
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from patient_transport_report.models import (
    PatientTransportReport,
    InformedConsent,
    CareTransferReport,
    SatisfactionSurvey,
    MedicationAdministration,
    PhysicalExam,
    Companion,
    OutgoingReceivingEntity,
    RequiredProcedures,
    Treatment,
    Result,
    ComplicationsTransfer,
    Patient
)
from patient_transport_report.domain_service import SaveReportDomainService
from patient_transport_report.types.typed_dict import SaveReportRequestData
from staff.models import (
    Healthcare, 
    Driver
)
from daily_monthly_inventory.models import Ambulance
from patient_transport_report.models import (
    Diagnosis, 
    IPS
)
from rest_framework.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

class SaveReportApplicationService:
    '''
    Application service for saving patient transport reports.
    Orchestrates the complete save/update process with transaction support.
    '''
    
    SUCCESS: int = 1
    FAILURE: int = -1    

    def __init__(self) -> None:
        self.domain_service: SaveReportDomainService = SaveReportDomainService()
    
    @transaction.atomic
    def save_report(
        self, 
        data: SaveReportRequestData, 
        user: User
    ) -> dict[str, Any]:
        '''
        Save or update patient transport report.
        
        Args:
            data: Validated request data
            user: Authenticated user
        
        Returns:
            dict: Response with report details and status
        '''
        try:
            report_id: int | None = data.get('report_id')
            result: dict
            if report_id:
                # UPDATE MODE
                result = self._update_existing_report(
                    report_id, 
                    data, 
                    user
                )
            else:
                # CREATE MODE
                result = self._create_new_report(
                    data, 
                    user
                )
            return {
                'response': result['message'],
                'msg': self.SUCCESS,
                'status_code_http': HTTP_200_OK,
                'report': result['report_data']
            }
        except PatientTransportReport.DoesNotExist:
            return {
                'response': f'Report with ID {report_id} not found',
                'msg': self.FAILURE,
                'status_code_http': HTTP_404_NOT_FOUND
            }
        except ValidationError as e:
            return {
                'response': 'Validation error',
                'msg': self.FAILURE,
                'status_code_http': HTTP_400_BAD_REQUEST,
                'errors': e.message_dict if hasattr(e, 'message_dict') else str(e)
            }
        except Exception as e:
            return {
                'response': f'Error saving report: {str(e)}',
                'msg': self.FAILURE,
                'status_code_http': HTTP_500_INTERNAL_SERVER_ERROR
            }
    
    def _create_new_report(
        self, 
        data: SaveReportRequestData, 
        user: User
    ) -> dict:
        '''Create new report with minimum required data'''
        sections_created: list[str] = []
        # 1. Validate attending_staff exists
        attending_staff_id: int = data.get('attending_staff')
        try:
            attending_staff: Healthcare = Healthcare.objects.get(
                base_staff_id=attending_staff_id
            )
        except Healthcare.DoesNotExist:
            raise ValidationError({
                'attending_staff': f'Personal de Salud con ID {attending_staff_id} no encontrado.'
            })
        # 2. Create Patient
        patient: Patient = self.domain_service.create_or_update_patient(
            data['patient'],
            None
        )
        sections_created.append('patient')
        # 3. Create PatientTransportReport (initially empty)
        report: PatientTransportReport = PatientTransportReport.objects.create(
            attending_staff=attending_staff,
            patient=patient,
            status='borrador',
            created_by=user,
            updated_by=user
        )
        # 4. Create InformedConsent if provided
        if 'informed_consent' in data and data['informed_consent']:
            informed_consent: InformedConsent | None = self._handle_informed_consent(
                data['informed_consent'],
                None,
                user
            )
            if informed_consent:
                report.informed_consent = informed_consent
                sections_created.append('informed_consent')
        # 5. Create CareTransferReport if provided
        if 'care_transfer_report' in data and data['care_transfer_report']:
            care_transfer: CareTransferReport | None = self._handle_care_transfer_report(
                data['care_transfer_report'],
                None,
                user
            )
            if care_transfer:
                report.care_transfer_report = care_transfer
                sections_created.append('care_transfer_report')
        # 6. Create SatisfactionSurvey if provided
        if 'satisfaction_survey' in data and data['satisfaction_survey']:
            satisfaction: SatisfactionSurvey | None = self._handle_satisfaction_survey(
                data['satisfaction_survey'],
                None,
                user
            )
            if satisfaction:
                report.satisfaction_survey = satisfaction
                sections_created.append('satisfaction_survey')
        # 7. Verify report completion
        completion_percentage: int
        completed: bool
        completion_percentage, completed = self.domain_service.get_report_completion_info(data)
        report.completion_percentage = completion_percentage
        if completed:
            report.status = 'completado'
        else:
            report.status = 'borrador'
        report.save()
        return {
            'message': 'Reporte creado exitosamente.',
            'report_data': self._build_response_data(
                report, 
                sections_created
            )
        }
    
    def _update_existing_report(
        self, 
        report_id: int, 
        data: SaveReportRequestData, 
        user: User
    ) -> dict:
        '''Update existing report'''
        report: PatientTransportReport = PatientTransportReport.objects.select_related(
            'attending_staff',
            'patient',
            'informed_consent',
            'care_transfer_report',
            'satisfaction_survey'
        ).get(id=report_id)
        sections_updated: list[str] = []
        # 1. Update Patient if data provided
        if 'patient' in data:
            patient: Patient = self.domain_service.create_or_update_patient(
                data['patient'], 
                report.patient
            )
            sections_updated.append('patient')
        # 2. Update/Create InformedConsent
        if 'informed_consent' in data:
            informed_consent: InformedConsent = self._handle_informed_consent(
                data['informed_consent'],
                report.informed_consent,
                user
            )
            if informed_consent and not report.informed_consent:
                report.informed_consent = informed_consent
                sections_updated.append('informed_consent')
            elif informed_consent:
                sections_updated.append('informed_consent')
        # 3. Update/Create CareTransferReport
        if 'care_transfer_report' in data:
            care_transfer: CareTransferReport = self._handle_care_transfer_report(
                data['care_transfer_report'],
                report.care_transfer_report,
                user
            )
            if care_transfer and not report.care_transfer_report:
                report.care_transfer_report = care_transfer
                sections_updated.append('care_transfer_report')
            elif care_transfer:
                sections_updated.append('care_transfer_report')
        # 4. Update/Create SatisfactionSurvey
        if 'satisfaction_survey' in data:
            satisfaction: SatisfactionSurvey = self._handle_satisfaction_survey(
                data['satisfaction_survey'],
                report.satisfaction_survey,
                user
            )
            if satisfaction and not report.satisfaction_survey:
                report.satisfaction_survey = satisfaction
                sections_updated.append('satisfaction_survey')
            elif satisfaction:
                sections_updated.append('satisfaction_survey')
        # 5. Update tracking
        report.updated_by = user
        # 6. Verify report completion
        completion_percentage: int
        completed: bool
        completion_percentage, completed = self.domain_service.get_report_completion_info(data)
        report.completion_percentage = completion_percentage
        if completed:
            report.status = 'completado'
        else:
            report.status = 'borrador'
        report.save()
        return {
            'message': 'Reporte actualizado exitosamente.',
            'report_data': self._build_response_data(report, sections_updated)
        }
    
    def _handle_informed_consent(
        self,
        data: dict,
        existing: InformedConsent | None,
        user: User
    ) -> InformedConsent:
        '''Handle InformedConsent creation/update'''
        # Handle outgoing entity
        outgoing_entity: OutgoingReceivingEntity | None = None
        if 'outgoing_entity' in data and data['outgoing_entity']:
            outgoing_entity = self.domain_service.create_or_update_entity(data['outgoing_entity'])
        # Handle required procedures
        required_procedures: RequiredProcedures | None = None
        if 'procedure' in data and data['procedure']:
            existing_procedures: RequiredProcedures | None = existing.required_procedures if existing else None
            required_procedures: RequiredProcedures | None = self.domain_service.create_or_update_required_procedures(
                data['procedure'],
                existing_procedures
            )
        # Handle medication administration
        medication_administration: MedicationAdministration | None = None
        if 'medication_administration' in data and data['medication_administration']:
            existing_medication = existing.medication_administration if existing else None
            medication_administration = self.domain_service.create_or_update_medication_administration(
                data['medication_administration'],
                existing_medication
            )
        # Prepare consent data
        consent_data: dict = {
            k: v for k, v in data.items() 
            if k not in [
                'outgoing_entity', 
                'procedure', 
                'medication_administration'
            ]
        }
        consent_data['outgoing_entity'] = outgoing_entity
        consent_data['required_procedures'] = required_procedures
        consent_data['medication_administration'] = medication_administration
        if existing:
            # Update existing
            for key, value in consent_data.items():
                setattr(existing, key, value)
            existing.updated_by = user
            existing.save()
            return existing
        else:
            # Create new
            consent: InformedConsent = InformedConsent.objects.create(
                **consent_data, 
                created_by=user, 
                updated_by=user
            )
            return consent
    
    def _handle_care_transfer_report(
        self,
        data: dict,
        existing: CareTransferReport | None,
        user: User
    ) -> CareTransferReport:
        '''Handle CareTransferReport creation/update'''
        # Validate FKs
        errors: dict[str, str] = self.domain_service.validate_foreign_keys(data)
        if errors:
            raise ValidationError(errors)
        # Resolve FKs
        driver: Driver | None = Driver.objects.get(base_staff_id=data['driver']) if data.get('driver') else None
        support_staff_name: str | None = data.get('support_staff')
        ambulance: Ambulance | None = Ambulance.objects.get(id=data['ambulance']) if data.get('ambulance') else None
        # Handle nested companion
        companion: Companion | None = None
        if 'companion' in data and data['companion']:
            companion = self.domain_service.create_or_update_companion(data['companion'])
        # Handle nested responsible
        responsible: Companion | None = None
        if 'responsible' in data and data['responsible']:
            responsible = self.domain_service.create_or_update_companion(data['responsible'])
        # Handle initial physical examination
        initial_exam: PhysicalExam | None = None
        if 'initial_physical_exam' in data and data['initial_physical_exam']:
            existing_initial: PhysicalExam | None = existing.initial_physical_exam if existing else None
            initial_exam = self.domain_service.create_or_update_physical_exam(
                data['initial_physical_exam'],
                existing_initial
            )
        # Handle final physical examination
        final_exam: PhysicalExam | None = None
        if 'final_physical_exam' in data and data['final_physical_exam']:
            existing_final: PhysicalExam | None = existing.final_physical_exam if existing else None
            final_exam = self.domain_service.create_or_update_physical_exam(
                data['final_physical_exam'],
                existing_final
            )
        # Handle treatment
        treatment: Treatment | None = None
        if 'treatment' in data and data['treatment']:
            existing_treatment: Treatment | None = existing.treatment if existing else None
            treatment = self.domain_service.create_or_update_treatment(
                data['treatment'],
                existing_treatment
            )
        # Handle result
        result: Result | None = None
        if 'result' in data and data['result']:
            existing_result: Result | None = existing.result if existing else None
            result = self.domain_service.create_or_update_result(
                data['result'],
                existing_result
            )
        # Handle complications
        complications: ComplicationsTransfer | None = None
        if 'complications_transfer' in data and data['complications_transfer']:
            existing_complications: ComplicationsTransfer | None = existing.complications_transfer if existing else None
            complications = self.domain_service.create_or_update_complications(
                data['complications_transfer'],
                existing_complications
            )
        # Handle receiving entity
        receiving_entity: OutgoingReceivingEntity | None = None
        if 'receiving_entity' in data and data['receiving_entity']:
            receiving_entity = self.domain_service.create_or_update_entity(data['receiving_entity'])
        # Prepare care transfer data
        care_data: dict = {
            k: v for k, v in data.items()
            if k not in [
                'driver', 'ambulance', 'companion',
                'responsible',
                'initial_physical_exam', 'final_physical_exam', 'treatment',
                'result', 'complications_transfer', 'receiving_entity', 
                'skin_condition', 'hemodynamic_status',
                'diagnosis_1', 'diagnosis_2', 'ips'
            ]
        }
        care_data.update({
            'driver': driver,
            'support_staff': support_staff_name,
            'ambulance': ambulance,
            'companion': companion,
            'responsible': responsible,
            'initial_physical_exam': initial_exam,
            'final_physical_exam': final_exam,
            'treatment': treatment,
            'result': result,
            'complications_transfer': complications,
            'receiving_entity': receiving_entity
        })
        # Handle FK fields directly (not nested)
        if 'diagnosis_1' in data and data['diagnosis_1']:
            care_data['diagnosis_1'] = Diagnosis.objects.get(id=data['diagnosis_1'])
        if 'diagnosis_2' in data and data['diagnosis_2']:
            care_data['diagnosis_2'] = Diagnosis.objects.get(id=data['diagnosis_2'])
        if 'ips' in data and data['ips']:
            care_data['ips'] = IPS.objects.get(id=data['ips'])
        if existing:
            # Update existing
            for key, value in care_data.items():
                setattr(existing, key, value)
            existing.updated_by = user
            existing.save()
            # Handle ManyToMany (frontend names: skin_condition, hemodynamic_status)
            if 'skin_condition' in data:
                skin_condition = data['skin_condition'] if data['skin_condition'] is not None else []
                existing.skin_conditions.set(skin_condition)
            if 'hemodynamic_status' in data:
                hemodynamic_status = data['hemodynamic_status'] if data['hemodynamic_status'] is not None else []
                existing.hemodynamic_statuses.set(hemodynamic_status)
            return existing
        else:
            # Create new
            care_transfer: CareTransferReport = CareTransferReport.objects.create(
                **care_data, 
                created_by=user, 
                updated_by=user
            )
            # Handle ManyToMany
            if 'skin_condition' in data:
                skin_condition = data['skin_condition'] if data['skin_condition'] is not None else []
                care_transfer.skin_conditions.set(skin_condition)
            if 'hemodynamic_status' in data:
                hemodynamic_status = data['hemodynamic_status'] if data['hemodynamic_status'] is not None else []
                care_transfer.hemodynamic_statuses.set(hemodynamic_status)
            return care_transfer
    
    def _handle_satisfaction_survey(
        self,
        data: dict,
        existing: SatisfactionSurvey | None,
        user: User
    ) -> SatisfactionSurvey:
        '''Handle SatisfactionSurvey creation/update'''
        if existing:
            # Update existing
            for key, value in data.items():
                setattr(existing, key, value)
            existing.updated_by = user
            existing.save()
            return existing
        else:
            # Create new
            return SatisfactionSurvey.objects.create(**data, created_by=user, updated_by=user)
    
    def _build_response_data(
        self, 
        report: PatientTransportReport, 
        sections_modified: list
    ) -> dict:
        '''Build response data structure'''
        return {
            'report_id': report.id,
            'status': report.status,
            'completion_percentage': report.completion_percentage,
            'has_patient_info': report.has_patient_info,
            'has_informed_consent': report.has_informed_consent,
            'has_care_transfer': report.has_care_transfer,
            'has_satisfaction_survey': report.has_satisfaction_survey,
            'sections_updated': sections_modified,
            'completed_at': report.updated_at.isoformat() if report.status == 'completado' else None,
            'completed_by': report.updated_by.username if report.status == 'completado' else None
        }
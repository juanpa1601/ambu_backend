from typing import Any
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from patient_transport_report.models import (
    PatientTransportReport,
    InformedConsent,
    CareTransferReport,
    SatisfactionSurvey
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

class SaveReportApplicationService:
    '''
    Application service for saving patient transport reports.
    Orchestrates the complete save/update process with transaction support.
    '''
    
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
            report_id = data.get('report_id')
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
                'msg': 1,
                'status_code': 200,
                'report': result['report_data']
            }
        except PatientTransportReport.DoesNotExist:
            return {
                'response': f'Report with ID {report_id} not found',
                'msg': -1,
                'status_code': 404
            }
        except ValidationError as e:
            return {
                'response': 'Validation error',
                'msg': -1,
                'status_code': 400,
                'errors': e.message_dict if hasattr(e, 'message_dict') else str(e)
            }
        except Exception as e:
            return {
                'response': f'Error saving report: {str(e)}',
                'msg': -1,
                'status_code': 500
            }
    
    def _create_new_report(
        self, 
        data: SaveReportRequestData, 
        user: User
    ) -> dict:
        '''Create new report with minimum required data'''
        sections_created = []
        # 1. Validate attending_staff exists
        attending_staff_id = data['care_transfer_report']['attending_staff']
        if not Healthcare.objects.filter(base_staff_id=attending_staff_id).exists():
            raise ValidationError({'attending_staff': f'Healthcare staff with ID {attending_staff_id} not found'})
        # 2. Create Patient
        patient = self.domain_service.create_or_update_patient(data['patient_data'])
        sections_created.append('patient')
        # 3. Create PatientTransportReport (initially empty)
        report = PatientTransportReport.objects.create(
            patient=patient,
            status='borrador',
            created_by=user,
            updated_by=user
        )
        # 4. Create CareTransferReport (with attending_staff)
        care_transfer = self._handle_care_transfer_report(
            data.get('care_transfer_report', {}),
            None,
            user
        )
        if care_transfer:
            report.care_transfer_report = care_transfer
            sections_created.append('care_transfer_report')
        # 5. Create InformedConsent if provided
        if 'informed_consent' in data:
            informed_consent = self._handle_informed_consent(
                data['informed_consent'],
                None,
                user
            )
            if informed_consent:
                report.informed_consent = informed_consent
                sections_created.append('informed_consent')
        # 6. Update tracking flags
        self.domain_service.update_tracking_flags(report)
        return {
            'message': 'Report created successfully',
            'report_data': self._build_response_data(report, sections_created)
        }
    
    def _update_existing_report(
        self, 
        report_id: int, 
        data: SaveReportRequestData, 
        user: User
    ) -> dict:
        '''Update existing report'''
        report = PatientTransportReport.objects.select_related(
            'patient',
            'informed_consent',
            'care_transfer_report',
            'satisfaction_survey'
        ).get(id=report_id)
        sections_updated = []
        # 1. Update Patient if data provided
        if 'patient_data' in data:
            self.domain_service.create_or_update_patient(data['patient_data'], report.patient)
            sections_updated.append('patient')
        # 2. Update/Create InformedConsent
        if 'informed_consent' in data:
            informed_consent = self._handle_informed_consent(
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
            care_transfer = self._handle_care_transfer_report(
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
            satisfaction = self._handle_satisfaction_survey(
                data['satisfaction_survey'],
                report.satisfaction_survey,
                user
            )
            if satisfaction and not report.satisfaction_survey:
                report.satisfaction_survey = satisfaction
                sections_updated.append('satisfaction_survey')
            elif satisfaction:
                sections_updated.append('satisfaction_survey')
        # 5. Handle status change
        if 'change_status_to' in data:
            requested_status = data['change_status_to']
            if requested_status == 'completado':
                if not report.can_complete():
                    raise ValidationError('Report cannot be completed. Missing required sections.')
                report.status = 'completado'
        # 6. Update tracking
        report.updated_by = user
        self.domain_service.update_tracking_flags(report)
        return {
            'message': 'Report updated successfully',
            'report_data': self._build_response_data(report, sections_updated)
        }
    
    def _handle_informed_consent(
        self,
        data: dict,
        existing: InformedConsent | None,
        user: User
    ) -> InformedConsent:
        '''Handle InformedConsent creation/update'''
        # Validate attending_staff
        attending_staff_id = data['attending_staff']
        attending_staff = Healthcare.objects.filter(base_staff_id=attending_staff_id).first()
        if not attending_staff:
            raise ValidationError({'attending_staff': f'Healthcare staff with ID {attending_staff_id} not found'})
        # Handle nested companion (responsible)
        responsible_companion = None
        if 'responsible' in data and data['responsible']:
            responsible_companion = self.domain_service.create_or_update_companion(data['responsible'])
        # Handle outgoing entity
        outgoing_entity = None
        if 'outgoing_entity' in data and data['outgoing_entity']:
            outgoing_entity = self.domain_service.create_or_update_entity(data['outgoing_entity'])
        # Prepare consent data
        consent_data = {k: v for k, v in data.items() if k not in ['responsible', 'outgoing_entity', 'attending_staff']}
        consent_data['attending_staff'] = attending_staff
        consent_data['responsible'] = responsible_companion
        consent_data['outgoing_entity'] = outgoing_entity
        if existing:
            # Update existing
            for key, value in consent_data.items():
                setattr(existing, key, value)
            existing.updated_by = user
            existing.save()
            return existing
        else:
            # Create new
            consent = InformedConsent.objects.create(**consent_data, created_by=user, updated_by=user)
            return consent
    
    def _handle_care_transfer_report(
        self,
        data: dict,
        existing: CareTransferReport | None,
        user: User
    ) -> CareTransferReport:
        '''Handle CareTransferReport creation/update'''
        # Validate FKs
        errors = self.domain_service.validate_foreign_keys(data)
        if errors:
            raise ValidationError(errors)
        # Resolve FKs
        attending_staff = Healthcare.objects.get(base_staff_id=data['attending_staff'])
        driver = Driver.objects.get(base_staff_id=data['driver']) if data.get('driver') else None
        support_staff = Healthcare.objects.get(base_staff_id=data['support_staff']) if data.get('support_staff') else None
        ambulance = Ambulance.objects.get(id=data['ambulance']) if data.get('ambulance') else None
        # Handle nested objects
        companion = None
        if 'companion' in data and data['companion']:
            companion = self.domain_service.create_or_update_companion(data['companion'])
        initial_exam = None
        if 'initial_physicial_examination' in data and data['initial_physicial_examination']:
            existing_initial = existing.initial_physicial_examination if existing else None
            initial_exam = self.domain_service.create_or_update_physical_exam(
                data['initial_physicial_examination'],
                existing_initial
            )
        final_exam = None
        if 'final_physical_examination' in data and data['final_physical_examination']:
            existing_final = existing.final_physical_examination if existing else None
            final_exam = self.domain_service.create_or_update_physical_exam(
                data['final_physical_examination'],
                existing_final
            )
        treatment = None
        if 'treatment' in data and data['treatment']:
            existing_treatment = existing.treatment if existing else None
            treatment = self.domain_service.create_or_update_treatment(
                data['treatment'],
                existing_treatment
            )
        result = None
        if 'result' in data and data['result']:
            existing_result = existing.result if existing else None
            result = self.domain_service.create_or_update_result(
                data['result'],
                existing_result
            )
        complications = None
        if 'complications_transfer' in data and data['complications_transfer']:
            existing_complications = existing.complications_transfer if existing else None
            complications = self.domain_service.create_or_update_complications(
                data['complications_transfer'],
                existing_complications
            )
        receiving_entity = None
        if 'receiving_entity' in data and data['receiving_entity']:
            receiving_entity = self.domain_service.create_or_update_entity(data['receiving_entity'])
        # Prepare care transfer data
        care_data = {
            k: v for k, v in data.items()
            if k not in [
                'attending_staff', 'driver', 'support_staff', 'ambulance', 'companion',
                'initial_physicial_examination', 'final_physical_examination', 'treatment',
                'result', 'complications_transfer', 'receiving_entity', 'skin_conditions',
                'hemodynamic_statuses', 'diagnosis_1', 'diagnosis_2', 'ips'
            ]
        }
        care_data.update({
            'attending_staff': attending_staff,
            'driver': driver,
            'support_staff': support_staff,
            'ambulance': ambulance,
            'companion': companion,
            'initial_physicial_examination': initial_exam,
            'final_physical_examination': final_exam,
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
            
            # Handle ManyToMany
            if 'skin_conditions' in data:
                existing.skin_conditions.set(data['skin_conditions'])
            if 'hemodynamic_statuses' in data:
                existing.hemodynamic_statuses.set(data['hemodynamic_statuses'])
            return existing
        else:
            # Create new
            care_transfer = CareTransferReport.objects.create(**care_data, created_by=user, updated_by=user)
            # Handle ManyToMany
            if 'skin_conditions' in data:
                care_transfer.skin_conditions.set(data['skin_conditions'])
            if 'hemodynamic_statuses' in data:
                care_transfer.hemodynamic_statuses.set(data['hemodynamic_statuses'])
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
            'can_complete': report.can_complete(),
            'has_patient_info': report.has_patient_info,
            'has_informed_consent': report.has_informed_consent,
            'has_care_transfer': report.has_care_transfer,
            'has_satisfaction_survey': report.has_satisfaction_survey,
            'sections_updated': sections_modified,
            'completed_at': report.updated_at.isoformat() if report.status == 'completado' else None,
            'completed_by': report.updated_by.username if report.status == 'completado' else None
        }
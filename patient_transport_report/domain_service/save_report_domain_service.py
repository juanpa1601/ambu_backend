from django.db import transaction
from django.contrib.auth.models import User
from patient_transport_report.models import (
    PatientTransportReport,
    Patient,
    InformedConsent,
    CareTransferReport,
    SatisfactionSurvey,
    Companion,
    OutgoingReceivingEntity,
    Glasgow,
    PhysicalExam,
    Treatment,
    Result,
    ComplicationsTransfer,
    SkinCondition,
    HemodynamicStatus
)
from staff.models import Healthcare, Driver
from daily_monthly_inventory.models import Ambulance
from patient_transport_report.types.typed_dict import (
    PatientData,
    CompanionData,
    EntityData,
    GlasgowData,
    PhysicalExamData,
    TreatmentData,
    ResultData,
    ComplicationsTransferData
)

class SaveReportDomainService:
    '''
    Domain service for managing patient transport report persistence.
    Handles creation and update of all related entities.
    '''
    
    @staticmethod
    def create_or_update_patient(
        patient_data: PatientData, 
        existing_patient: Patient | None = None
    ) -> Patient:
        '''Create new patient or update existing one'''
        if existing_patient:
            # Update existing
            for key, value in patient_data.items():
                setattr(existing_patient, key, value)
            existing_patient.save()
            return existing_patient
        else:
            # Create new
            return Patient.objects.create(**patient_data)
    
    @staticmethod
    def create_or_update_companion(companion_data: CompanionData) -> Companion | None:
        '''Create companion if data provided'''
        if not companion_data or not companion_data.get('full_name'):
            return None
        # Check if companion exists by document
        document_number: str | None = companion_data.get('document_number')
        if document_number:
            companion: Companion
            created: bool
            companion, created = Companion.objects.get_or_create(
                document_number=document_number,
                defaults=companion_data
            )
            if not created:
                # Update existing
                for key, value in companion_data.items():
                    setattr(companion, key, value)
                companion.save()
            return companion
        else:
            # Create without uniqueness check
            return Companion.objects.create(**companion_data)
    
    @staticmethod
    def create_or_update_entity(entity_data: EntityData) -> OutgoingReceivingEntity | None:
        '''Create outgoing/receiving entity if data provided'''
        if not entity_data or not entity_data.get('name'):
            return None
        # Check if entity exists by document
        document: str | None = entity_data.get('document')
        if document:
            entity: OutgoingReceivingEntity
            created: bool
            entity, created = OutgoingReceivingEntity.objects.get_or_create(
                document=document,
                defaults=entity_data
            )
            if not created:
                # Update existing
                for key, value in entity_data.items():
                    setattr(entity, key, value)
                entity.save()
            return entity
        else:
            # Create without uniqueness check
            return OutgoingReceivingEntity.objects.create(**entity_data)
    
    @staticmethod
    def create_or_update_glasgow(
        glasgow_data: GlasgowData, 
        existing_glasgow: Glasgow | None = None
    ) -> Glasgow | None:
        '''Create or update Glasgow scale'''
        if not glasgow_data:
            return existing_glasgow
        if existing_glasgow:
            # Update existing
            for key, value in glasgow_data.items():
                setattr(existing_glasgow, key, value)
            existing_glasgow.save()
            return existing_glasgow
        else:
            # Create new
            return Glasgow.objects.create(**glasgow_data)
    
    def create_or_update_physical_exam(
        self,
        exam_data: PhysicalExamData,
        existing_exam: PhysicalExam | None = None
    ) -> PhysicalExam | None:
        '''Create or update physical examination'''
        if not exam_data:
            return existing_exam
        # Handle nested Glasgow
        glasgow_data: GlasgowData | None = exam_data.pop('glasgow', None)
        glasgow: Glasgow | None = None
        if glasgow_data:
            existing_glasgow: Glasgow | None = existing_exam.glasgow if existing_exam else None
            glasgow: Glasgow | None = self.create_or_update_glasgow(glasgow_data, existing_glasgow)
        if existing_exam:
            # Update existing
            for key, value in exam_data.items():
                setattr(existing_exam, key, value)
            if glasgow:
                existing_exam.glasgow = glasgow
            existing_exam.save()
            return existing_exam
        else:
            # Create new
            exam = PhysicalExam.objects.create(glasgow=glasgow, **exam_data)
            return exam
    
    @staticmethod
    def create_or_update_treatment(
        treatment_data: TreatmentData,
        existing_treatment: Treatment | None = None
    ) -> Treatment | None:
        '''Create or update treatment'''
        if not treatment_data:
            return existing_treatment
        if existing_treatment:
            # Update existing
            for key, value in treatment_data.items():
                setattr(existing_treatment, key, value)
            existing_treatment.save()
            return existing_treatment
        else:
            # Create new
            return Treatment.objects.create(**treatment_data)
    
    @staticmethod
    def create_or_update_result(
        result_data: ResultData,
        existing_result: Result | None = None
    ) -> Result | None:
        '''Create or update result'''
        if not result_data:
            return existing_result
        if existing_result:
            # Update existing
            for key, value in result_data.items():
                setattr(existing_result, key, value)
            existing_result.save()
            return existing_result
        else:
            # Create new
            return Result.objects.create(**result_data)
    
    @staticmethod
    def create_or_update_complications(
        complications_data: ComplicationsTransferData,
        existing_complications: ComplicationsTransfer | None = None
    ) -> ComplicationsTransfer | None:
        '''Create or update complications'''
        if not complications_data:
            return existing_complications
        if existing_complications:
            # Update existing
            for key, value in complications_data.items():
                setattr(existing_complications, key, value)
            existing_complications.save()
            return existing_complications
        else:
            # Create new
            return ComplicationsTransfer.objects.create(**complications_data)
    
    @staticmethod
    def validate_foreign_keys(data: dict) -> dict:
        '''Validate that all FK IDs exist in database'''
        errors: dict = {}
        # Validate Healthcare (attending_staff)
        if 'attending_staff' in data:
            if not Healthcare.objects.filter(base_staff_id=data['attending_staff']).exists():
                errors['attending_staff'] = f'Healthcare staff with ID {data["attending_staff"]} not found'
        # Validate Driver
        if 'driver' in data and data['driver']:
            if not Driver.objects.filter(base_staff_id=data['driver']).exists():
                errors['driver'] = f'Driver with ID {data["driver"]} not found'
        # Validate Ambulance
        if 'ambulance' in data and data['ambulance']:
            if not Ambulance.objects.filter(id=data['ambulance']).exists():
                errors['ambulance'] = f'Ambulance with ID {data["ambulance"]} not found'
        return errors
    
    @staticmethod
    def update_tracking_flags(report: PatientTransportReport) -> None:
        '''Update completion tracking flags'''
        report.has_patient_info = bool(report.patient_id)
        report.has_informed_consent = bool(report.informed_consent_id)
        report.has_care_transfer = bool(report.care_transfer_report_id)
        report.has_satisfaction_survey = bool(report.satisfaction_survey_id)
        report.completion_percentage = report.calculate_completion()
        report.save()
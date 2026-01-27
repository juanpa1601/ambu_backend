from patient_transport_report.models import (
    Patient,
    PatientHistory,
    InsuranceProvider,
    RequiredProcedures,
    MedicationAdministration,
    Companion,
    OutgoingReceivingEntity,
    Glasgow,
    PhysicalExam,
    Treatment,
    Result,
    ComplicationsTransfer
)
from patient_transport_report.types.typed_dict import (
    PatientData,
    PatientHistoryData,
    InsuranceProviderData,
    RequiredProceduresData,
    MedicationAdministrationData,
    CompanionData,
    EntityData,
    GlasgowData,
    PhysicalExamData,
    TreatmentData,
    ResultData,
    ComplicationsTransferData
)
from patient_transport_report.models import PatientTransportReport
from staff.models import (
    Healthcare, 
    Driver
)
from daily_monthly_inventory.models import Ambulance

class SaveReportDomainService:
    '''
    Domain service for managing patient transport report persistence.
    Handles creation and update of all related entities.
    '''
    
    @staticmethod
    def create_or_update_patient_history(
        history_data: PatientHistoryData,
        existing_history: PatientHistory | None = None
    ) -> PatientHistory | None:
        '''Create or update patient history'''

        if not history_data:
            return existing_history
        if existing_history:
            # Update existing
            for key, value in history_data.items():
                setattr(existing_history, key, value)
            existing_history.save()
            return existing_history
        else:
            # Create new
            return PatientHistory.objects.create(**history_data)
    
    @staticmethod
    def create_or_update_insurance_provider(
        insurance_data: InsuranceProviderData,
        existing_insurance: InsuranceProvider | None = None
    ) -> InsuranceProvider | None:
        '''Create or update insurance provider'''

        if not insurance_data:
            return existing_insurance
        if existing_insurance:
            # Update existing
            for key, value in insurance_data.items():
                setattr(existing_insurance, key, value)
            existing_insurance.save()
            return existing_insurance
        else:
            # Create new
            return InsuranceProvider.objects.create(**insurance_data)
    
    @staticmethod
    def create_or_update_patient(
        patient_data: PatientData, 
        existing_patient: Patient | None = None
    ) -> Patient:
        '''Create new patient or update existing one'''

        # Extract nested objects
        history_data: PatientHistoryData | None = patient_data.pop('patient_history', None)
        insurance_data: InsuranceProviderData | None = patient_data.pop('insurance_provider', None)
        history: PatientHistory | None = None
        insurance: InsuranceProvider | None = None
        # Handle patient_age -> age mapping
        if 'patient_age' in patient_data:
            patient_data['age'] = patient_data.pop('patient_age')
        if existing_patient:
            # Update patient history
            if history_data:
                history = SaveReportDomainService.create_or_update_patient_history(
                    history_data,
                    existing_patient.patient_history
                )
                patient_data['patient_history'] = history
            # Update insurance provider
            if insurance_data:
                insurance = SaveReportDomainService.create_or_update_insurance_provider(
                    insurance_data,
                    existing_patient.insurance_provider
                )
                patient_data['insurance_provider'] = insurance
            # Update existing patient
            for key, value in patient_data.items():
                setattr(existing_patient, key, value)
            existing_patient.save()
            return existing_patient
        else:
            # Create new patient with nested objects
            history = SaveReportDomainService.create_or_update_patient_history(history_data) if history_data else None
            insurance = SaveReportDomainService.create_or_update_insurance_provider(insurance_data) if insurance_data else None
            patient_data['patient_history'] = history
            patient_data['insurance_provider'] = insurance
            return Patient.objects.create(**patient_data)
    
    @staticmethod
    def create_or_update_required_procedures(
        procedure_data: RequiredProceduresData,
        existing_procedures: RequiredProcedures | None = None
    ) -> RequiredProcedures | None:
        '''Create or update required procedures'''

        if not procedure_data:
            return existing_procedures
        if existing_procedures:
            # Update existing
            for key, value in procedure_data.items():
                setattr(existing_procedures, key, value)
            existing_procedures.save()
            return existing_procedures
        else:
            # Create new
            return RequiredProcedures.objects.create(**procedure_data)
    
    @staticmethod
    def create_or_update_medication_administration(
        medication_data: MedicationAdministrationData,
        existing_medication: MedicationAdministration | None = None
    ) -> MedicationAdministration | None:
        '''Create or update medication administration'''

        if not medication_data:
            return existing_medication
        if existing_medication:
            # Update existing
            for key, value in medication_data.items():
                setattr(existing_medication, key, value)
            existing_medication.save()
            return existing_medication
        else:
            # Create new
            return MedicationAdministration.objects.create(**medication_data)
    
    @staticmethod
    def create_or_update_companion(companion_data: CompanionData) -> Companion | None:
        '''Create companion if data provided'''

        if not companion_data or not companion_data.get('name'):
            return None
        # Map frontend field names to model field names
        mapped_data: dict[str, str | None] = {
            'full_name': companion_data.get('name'),
            'document_number': companion_data.get('identification_number'),
            'relationship': companion_data.get('kindship'),
            'phone': companion_data.get('phone_number')
        }
        # Check if companion exists by document
        document_number: str | None = mapped_data.get('document_number')
        if document_number:
            companion, created = Companion.objects.get_or_create(
                document_number=document_number,
                defaults=mapped_data
            )
            if not created:
                # Update existing
                for key, value in mapped_data.items():
                    setattr(companion, key, value)
                companion.save()
            return companion
        else:
            # Create without uniqueness check
            return Companion.objects.create(**mapped_data)
    
    @staticmethod
    def create_or_update_entity(entity_data: EntityData) -> OutgoingReceivingEntity | None:
        '''Create outgoing/receiving entity if data provided'''

        if not entity_data or not entity_data.get('name'):
            return None
        # Check if entity exists by document
        document: str | None = entity_data.get('document')
        if document:
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
        glasgow_data: GlasgowData | None,
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
    
    @staticmethod
    def create_or_update_physical_exam(
        exam_data: PhysicalExamData | None = None,
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
            glasgow = SaveReportDomainService.create_or_update_glasgow(
                glasgow_data, 
                existing_glasgow
            )
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
            exam: PhysicalExam = PhysicalExam.objects.create(
                glasgow=glasgow, 
                **exam_data
            )
            return exam
    
    @staticmethod
    def create_or_update_treatment(
        treatment_data: TreatmentData,
        existing_treatment: Treatment | None = None
    ) -> Treatment | None:
        '''Create or update treatment'''

        if not treatment_data:
            return existing_treatment
        # Map frontend field name to model field name
        if 'liters_minute' in treatment_data:
            treatment_data['liter_minute'] = treatment_data.pop('liters_minute')
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
        # Map frontend field name to model field name
        if 'description_complications' in complications_data:
            complications_data['description_complication'] = complications_data.pop('description_complications')
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
    def validate_foreign_keys(data: dict) -> dict[str, str]:
        '''Validate that all FK IDs exist in database'''

        errors: dict[str, str] = {}
        # Validate Healthcare (attending_staff)
        if 'attending_staff' in data:
            if not Healthcare.objects.filter(base_staff_id=data['attending_staff']).exists():
                errors['attending_staff'] = f"Personal de Salud con ID {data['attending_staff']} no encontrado"
        # Validate Driver
        if 'driver' in data and data['driver']:
            if not Driver.objects.filter(base_staff_id=data['driver']).exists():
                errors['driver'] = f"Conductor con ID {data['driver']} no encontrado"
        # Validate Support Staff
        if 'support_staff' in data and data['support_staff']:
            if not Healthcare.objects.filter(base_staff_id=data['support_staff']).exists():
                errors['support_staff'] = f"Personal de Apoyo con ID {data['support_staff']} no encontrado"
        # Validate Ambulance
        if 'ambulance' in data and data['ambulance']:
            if not Ambulance.objects.filter(id=data['ambulance']).exists():
                errors['ambulance'] = f"Ambulancia con ID {data['ambulance']} no encontrada"
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
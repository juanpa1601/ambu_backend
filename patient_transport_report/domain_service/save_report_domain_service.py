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
        '''
        Create new patient or update existing one.
        
        Args:
            patient_data: Patient data from request
            existing_patient: Existing patient instance (optional)
        
        Returns:
            Patient: Created or updated patient instance
        '''
        # Extract nested objects
        history_data: PatientHistoryData | None = patient_data.pop('patient_history', None)
        insurance_data: InsuranceProviderData | None = patient_data.pop('insurance_provider', None)
        history: PatientHistory | None = None
        insurance: InsuranceProvider | None = None
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
            # Update existing patient fields
            for key, value in patient_data.items():
                setattr(existing_patient, key, value)
            existing_patient.save()
            return existing_patient
        else:
            # Create nested objects
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
            'name': companion_data.get('name'),
            'identification_number': companion_data.get('identification_number'),
            'kindship': companion_data.get('kindship'),
            'phone_number': companion_data.get('phone_number')
        }
        # Check if companion exists by document
        identification_number: str | None = mapped_data.get('identification_number')
        if identification_number:
            companion, created = Companion.objects.get_or_create(
                identification_number=identification_number,
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
            treatment_data['liters_minute'] = treatment_data.pop('liters_minute')
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
        # Validate Ambulance
        if 'ambulance' in data and data['ambulance']:
            if not Ambulance.objects.filter(id=data['ambulance']).exists():
                errors['ambulance'] = f"Ambulancia con ID {data['ambulance']} no encontrada"
        return errors
    
    @staticmethod
    def get_report_completion_info(data: dict) -> tuple[int, bool]:
        '''
        Evaluate whether all required fields in the report are complete..
        Returns True if all required fields have a value other than None and "".
        '''
        # List of paths to required fields (using your structure)
        required_fields: list[list[str]] = [
            ['attending_staff'],
            # Patient
            ['patient', 'patient_name'],
            ['patient', 'identification_type'],
            ['patient', 'other_identification_type'],
            ['patient', 'identification_number'],
            ['patient', 'birth_date'],
            ['patient', 'sex'],
            ['patient', 'home_address'],
            ['patient', 'residence_city'],
            ['patient', 'cell_phone'],
            ['patient', 'patient_history', 'has_pathology'],
            ['patient', 'patient_history', 'has_allergies'],
            ['patient', 'patient_history', 'has_surgeries'],
            ['patient', 'patient_history', 'has_medicines'],
            ['patient', 'patient_history', 'tobacco_use'],
            ['patient', 'patient_history', 'substance_use'],
            ['patient', 'patient_history', 'alcohol_use'],
            ['patient', 'insurance_provider', 'coverage_type'],
            ['patient', 'insurance_provider', 'provider_name'],
            ['patient', 'membership_category'],
            # Informed consent
            ['informed_consent', 'consent_timestamp'],
            ['informed_consent', 'guardian_type'],
            ['informed_consent', 'guardian_name'],
            ['informed_consent', 'responsible_for'],
            ['informed_consent', 'guardian_id_type'],
            ['informed_consent', 'guardian_id_number'],
            ['informed_consent', 'administers_medications'],
            ['informed_consent', 'service_type'],
            ['informed_consent', 'attending_staff_signature'],            
            # Care transfer report
            ['care_transfer_report', 'patient_one_of'],
            ['care_transfer_report', 'service_type'],
            ['care_transfer_report', 'initial_address'],
            ['care_transfer_report', 'transfer_type'],
            ['care_transfer_report', 'driver'],
            ['care_transfer_report', 'ambulance'],
            ['care_transfer_report', 'initial_physical_exam', 'systolic'],
            ['care_transfer_report', 'initial_physical_exam', 'diastolic'],
            ['care_transfer_report', 'initial_physical_exam', 'heart_rate'],
            ['care_transfer_report', 'initial_physical_exam', 'respiratory_rate'],
            ['care_transfer_report', 'initial_physical_exam', 'oxygen_saturation'],
            ['care_transfer_report', 'initial_physical_exam', 'temperature'],
            ['care_transfer_report', 'initial_physical_exam', 'glasgow', 'motor'],
            ['care_transfer_report', 'initial_physical_exam', 'glasgow', 'motor_text'],
            ['care_transfer_report', 'initial_physical_exam', 'glasgow', 'verbal'],
            ['care_transfer_report', 'initial_physical_exam', 'glasgow', 'verbal_text'],
            ['care_transfer_report', 'initial_physical_exam', 'glasgow', 'eyes_opening'],
            ['care_transfer_report', 'initial_physical_exam', 'glasgow', 'eyes_opening_text'],
            ['care_transfer_report', 'skin_condition'],
            ['care_transfer_report', 'hemodynamic_status'],
            ['care_transfer_report', 'treatment', 'monitors_vital_signs'],
            ['care_transfer_report', 'treatment', 'oxygen'],
            ['care_transfer_report', 'diagnosis_1'],
            ['care_transfer_report', 'ips'],
            ['care_transfer_report', 'complications_transfer', 'description_complication'],
            ['care_transfer_report', 'notes'],
            ['care_transfer_report', 'final_physical_exam', 'systolic'],
            ['care_transfer_report', 'final_physical_exam', 'diastolic'],
            ['care_transfer_report', 'final_physical_exam', 'heart_rate'],
            ['care_transfer_report', 'final_physical_exam', 'respiratory_rate'],
            ['care_transfer_report', 'final_physical_exam', 'oxygen_saturation'],
            ['care_transfer_report', 'final_physical_exam', 'temperature'],
            ['care_transfer_report', 'final_physical_exam', 'glasgow', 'motor'],
            ['care_transfer_report', 'final_physical_exam', 'glasgow', 'motor_text'],
            ['care_transfer_report', 'final_physical_exam', 'glasgow', 'verbal'],
            ['care_transfer_report', 'final_physical_exam', 'glasgow', 'verbal_text'],
            ['care_transfer_report', 'final_physical_exam', 'glasgow', 'eyes_opening'],
            ['care_transfer_report', 'final_physical_exam', 'glasgow', 'eyes_opening_text'],            
            # satisfaction_survey
            ['satisfaction_survey', 'satisfaction_survey_conducted'],
        ]

        # Campos de hora según transfer_type
        hour_fields_double: list[list[str]] = [
            ['care_transfer_report', 'patient_arrival_time'],
            ['care_transfer_report', 'patient_departure_time'],
            ['care_transfer_report', 'arrival_time_patient'],
            ['care_transfer_report', 'double_departure_time'],
            ['care_transfer_report', 'double_arrival_time'],
            ['care_transfer_report', 'end_attention_time'],
        ]
        hour_fields_simple: list[list[str]] = [
            ['care_transfer_report', 'patient_arrival_time'],
            ['care_transfer_report', 'patient_departure_time'],
            ['care_transfer_report', 'arrival_time_patient'],
            ['care_transfer_report', 'end_attention_time'],
        ]

        # Helper para obtener valor anidado
        def get_nested(
            data: dict, 
            keys: list[str]
        ) -> dict | None:
            for key in keys:
                if isinstance(data, dict) and key in data:
                    data = data[key]
                else:
                    return None
            return data
        # 1. Determine transfer_type
        transfer_type: dict | None = get_nested(data, ['care_transfer_report', 'transfer_type'])
        if transfer_type == 'traslado asistencial básico-doble':
            required_fields += hour_fields_double
        elif transfer_type == 'traslado asistencial básico-sencillo':
            required_fields += hour_fields_simple
        # 2. Validate procedure: at least one must be marked (not None or "")
        procedure: dict | None = get_nested(data, ['informed_consent', 'procedure'])
        procedure_fields: list[str] = ['immobilization', 'stretcher_transfer', 'ambulance_transport', 'assessment']
        procedure_valid: bool = False
        if isinstance(procedure, dict):
            for pf in procedure_fields:
                if procedure.get(pf) not in (None, ""):
                    procedure_valid = True
                    break
        # If none, it is considered incomplete
        total: int = len(required_fields) + 1  # +1 for procedure
        completed: int = 0
        # 3. Count completed fields
        for path in required_fields:
            value: dict | None = get_nested(data, path)
            if value not in (None, ""):
                completed += 1
        if procedure_valid:
            completed += 1
        percentage: int = int((completed / total) * 100) if total > 0 else 0
        is_complete: bool = (percentage == 100)
        return percentage, is_complete
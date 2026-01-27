"""
Component serializers for inventory category models.

These reusable serializers provide proper field-level validation for all
category objects in inventory operations (create, update, detail responses).
They replace the generic DictField approach with type-safe, validated serializers.
"""

from .additionals_serializer import AdditionalsSerializer
from .surgical_serializer import SurgicalSerializer
from .respiratory_serializer import RespiratorySerializer
from .biomedical_equipment_serializer import BiomedicalEquipmentSerializer
from .accessories_serializer import AccessoriesSerializer
from .immobilization_safety_serializer import ImmobilizationAndSafetySerializer
from .pediatric_serializer import PediatricSerializer
from .circulatory_serializer import CirculatorySerializer
from .ambulance_kit_serializer import AmbulanceKitSerializer
from .accessories_case_serializer import AccessoriesCaseSerializer
from .shift_serializer import ShiftSerializer

__all__ = [
    "AdditionalsSerializer",
    "SurgicalSerializer",
    "RespiratorySerializer",
    "BiomedicalEquipmentSerializer",
    "AccessoriesSerializer",
    "ImmobilizationAndSafetySerializer",
    "PediatricSerializer",
    "CirculatorySerializer",
    "AmbulanceKitSerializer",
    "AccessoriesCaseSerializer",
    "ShiftSerializer",
]

from django.conf import settings
from django.db import models

from .accessories import Accessories
from .accessories_case import AccessoriesCase
from .additionals import Additionals
from .ambulance import Ambulance
from .ambulance_kit import AmbulanceKit
from .biomedical_equipment import BiomedicalEquipment
from .circulatory import Circulatory
from .immobilization_safety import ImmobilizationAndSafety
from .pediatric import Pediatric
from .respiratory import Respiratory
from .surgical import Surgical
from .shift import Shift
from core.models import AuditedModel, ActiveManager


class DailyMonthlyInventory(AuditedModel):
    biomedical_equipment = models.ForeignKey(
        BiomedicalEquipment, on_delete=models.CASCADE, null=True, blank=True
    )
    accessories_case = models.ForeignKey(
        AccessoriesCase,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    respiratory = models.ForeignKey(
        Respiratory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    immobilization_and_safety = models.ForeignKey(
        ImmobilizationAndSafety,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    surgical = models.ForeignKey(
        Surgical,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    accessories = models.ForeignKey(
        Accessories,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    additionals = models.ForeignKey(
        Additionals,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    pediatric = models.ForeignKey(
        Pediatric,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    circulatory = models.ForeignKey(
        Circulatory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    ambulance_kit = models.ForeignKey(
        AmbulanceKit,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    system_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ambulance = models.ForeignKey(
        Ambulance,
        on_delete=models.SET_NULL,
        null=True,
        max_length=128,
        blank=True,
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    support_staff = models.TextField(
        blank=True,
        null=True,
    )

    date = models.DateField()

    observations = models.TextField(blank=True, default="")

    is_completed = models.BooleanField(default=False)

    # Managers
    objects = ActiveManager()  # Excluye is_deleted=True por defecto
    all_objects = models.Manager()  # Incluye todos los registros

    def __str__(self):
        return f"DailyMonthlyInventory {self.date} ({self.pk})"

    def calculate_is_completed(self) -> bool:
        """
        Determina si el inventario está completo.

        Reglas:
        - Campos obligatorios del inventario: date, ambulance, shift, system_user
        - Exige que todas las relaciones de equipamiento no sean None
        - Para cada objeto relacionado, valida todos sus campos de modelo:
            - Los campos PK/autoincrement se ignoran.
            - `None` o strings vacíos cuentan como "vacío" -> no completado.
            - Valores numéricos (incluyendo 0) y booleanos se consideran válidos.
        - Campos opcionales que NO se validan: support_staff, observations, observations_comments
        """
        # Campos opcionales que se ignoran en la validación
        optional_fields = ['observations_comments']
        
        # Validar campos obligatorios del inventario principal
        if self.date is None:
            return False
        if self.ambulance is None:
            return False
        if self.shift is None:
            return False
        if self.system_user is None:
            return False

        # Relaciones de equipamiento a revisar (todas obligatorias)
        related_attrs = [
            "accessories",
            "accessories_case",
            "additionals",
            "ambulance_kit",
            "biomedical_equipment",
            "circulatory",
            "immobilization_and_safety",
            "pediatric",
            "respiratory",
            "surgical",
        ]

        for attr in related_attrs:
            rel_obj = getattr(self, attr, None)
            if rel_obj is None:
                return False

            # Inspeccionar cada campo del modelo relacionado
            for field in rel_obj._meta.fields:
                # Ignorar PK/autoincrement y campos auto generados
                if getattr(field, "primary_key", False):
                    continue
                
                # Ignorar campos opcionales específicos
                if field.name in optional_fields:
                    continue
                    
                # Obtener valor
                value = getattr(rel_obj, field.name, None)
                # None => incompleto
                if value is None:
                    return False
                # Cadenas vacías => incompleto
                if isinstance(value, str) and value.strip() == "":
                    return False
                # Para otros tipos (int, bool, float, date, ...) asumimos que el valor presente es válido

        # Si pasó todas las comprobaciones, está completo
        return True

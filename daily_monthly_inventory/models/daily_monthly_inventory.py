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


class DailyMonthlyInventory(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True)

    is_completed = models.BooleanField(default=False)

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    def __str__(self):
        return f"DailyMonthlyInventory {self.date} ({self.pk})"

    def calculate_is_completed(self) -> bool:
        """
        Determina si el inventario está completo.

        Reglas:
        - Exige que las relaciones principales no sean None (p. ej. biomedical_equipment, surgical, ...).
        - Para cada objeto relacionado, valida todos sus campos de modelo:
            - Los campos PK/autoincrement se ignoran.
            - `None` o strings vacíos cuentan como "vacío" -> no completado.
            - Valores numéricos (incluyendo 0) y booleanos se consideran válidos.
        - No tiene en cuenta `support_staff` ni `observations` del propio inventario.
        """
        # relaciones a revisar
        related_attrs = [
            "biomedical_equipment",
            "surgical",
            "accessories_case",
            "respiratory",
            "immobilization_and_safety",
            "accessories",
            "additionals",
            "pediatric",
            "circulatory",
            "ambulance_kit",
        ]

        # date y ambulance son obligatorios para considerar completado
        if self.date is None or self.ambulance is None:
            return False

        for attr in related_attrs:
            rel_obj = getattr(self, attr, None)
            if rel_obj is None:
                return False

            # inspeccionar cada campo del modelo relacionado
            for field in rel_obj._meta.fields:
                # ignorar PK/autoincrement y campos auto generados
                if getattr(field, "primary_key", False):
                    continue
                # obtener valor
                value = getattr(rel_obj, field.name, None)
                # None => incompleto
                if value is None:
                    return False
                # cadenas vacías => incompleto
                if isinstance(value, str) and value.strip() == "":
                    return False
                # para otros tipos (int, bool, float, date, ...) asumimos que el valor presente es válido

        # si pasó todas las comprobaciones, está completo
        return True

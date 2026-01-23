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
        AccessoriesCase, on_delete=models.CASCADE, null=True, blank=True
    )
    respiratory = models.ForeignKey(
        Respiratory, on_delete=models.CASCADE, null=True, blank=True
    )
    immobilization_and_safety = models.ForeignKey(
        ImmobilizationAndSafety, on_delete=models.CASCADE, null=True, blank=True
    )
    surgical = models.ForeignKey(
        Surgical, on_delete=models.CASCADE, null=True, blank=True
    )
    accessories = models.ForeignKey(
        Accessories, on_delete=models.CASCADE, null=True, blank=True
    )
    additionals = models.ForeignKey(
        Additionals, on_delete=models.CASCADE, null=True, blank=True
    )
    pediatric = models.ForeignKey(
        Pediatric, on_delete=models.CASCADE, null=True, blank=True
    )
    circulatory = models.ForeignKey(
        Circulatory, on_delete=models.CASCADE, null=True, blank=True
    )
    ambulance_kit = models.ForeignKey(
        AmbulanceKit, on_delete=models.CASCADE, null=True, blank=True
    )

    system_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
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
        default="",
    )

    date = models.DateField()

    observations = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"DailyMonthlyInventory {self.date} ({self.pk})"

    def calculate_is_completed(self) -> bool:
        """
        Check if the inventory is complete.
        An inventory is considered complete when all equipment categories have data,
        excluding optional fields like support_staff and observations.

        Returns:
            bool: True if all required fields are filled, False otherwise
        """
        # Check if all equipment categories exist (not None)
        return all(
            [
                self.biomedical_equipment is not None,
                self.surgical is not None,
                self.accessories_case is not None,
                self.respiratory is not None,
                self.immobilization_and_safety is not None,
                self.accessories is not None,
                self.additionals is not None,
                self.pediatric is not None,
                self.circulatory is not None,
                self.ambulance_kit is not None,
            ]
        )

from django.db import models
from django.conf import settings

from .biomedical_equipment import BiomedicalEquipment
from .surgical import Surgical
from .accessories_case import AccessoriesCase
from .respiratory import Respiratory
from .immobilization_safety import ImmobilizationAndSafety
from .accessories import Accessories
from .additionals import Additionals
from .pediatric import Pediatric
from .circulatory import Circulatory
from .ambulance_kit import AmbulanceKit
from .ambulance import Ambulance


class DailyMonthlyInventory(models.Model):
    biomedical_equipment = models.ForeignKey(
        BiomedicalEquipment,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    accessories_case = models.ForeignKey(
        AccessoriesCase,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    respiratory = models.ForeignKey(
        Respiratory,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    immobilization_and_safety = models.ForeignKey(
        ImmobilizationAndSafety,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    surgical = models.ForeignKey(
        Surgical,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    accessories = models.ForeignKey(
        Accessories,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    additionals = models.ForeignKey(
        Additionals,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    pediatric = models.ForeignKey(
        Pediatric,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    circulatory = models.ForeignKey(
        Circulatory,
         on_delete=models.CASCADE,
          null=True,
           blank=True
    )
    ambulance_kit = models.ForeignKey(
        AmbulanceKit,
         on_delete=models.CASCADE,
          null=True,
           blank=True
    )

    system_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ambulance = models.ForeignKey(
        Ambulance,
        on_delete=models.SET_NULL,
        null = True,
        max_length=128,
        blank=True,
        default=''
    )

    date = models.DateField()

    observations = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DailyMonthlyInventory {self.date} ({self.pk})"

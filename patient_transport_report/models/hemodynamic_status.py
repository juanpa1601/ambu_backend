from django.db import models
from core.models import TimeStampedModel

class HemodynamicStatus(TimeStampedModel):
    '''
    Catalog of possible hemodynamic statuses.
    '''
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Hemodynamic status name (e.g., "Estable", "Inestable", "Shock", "Compensado")'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this option is available for selection'
    )
    order = models.IntegerField(
        default=0,
        help_text='Order for displaying hemodynamic statuses'
    )

    class Meta:
        verbose_name = 'Hemodynamic Status'
        verbose_name_plural = 'Hemodynamic Statuses'
        ordering = ['order']
    
    def __str__(self):
        return self.name
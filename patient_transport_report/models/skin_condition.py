from django.db import models
from core.models import TimeStampedModel

class SkinCondition(TimeStampedModel):
    '''
    Catalog of skin conditions.
    Lightweight audit (timestamps only, no user tracking).
    '''
    name = models.CharField(
        max_length=100,
        unique=True
    )
    order = models.IntegerField(
        default=0,
        help_text='Order for displaying skin conditions'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this option is available for selection'
    )
    
    class Meta:
        verbose_name = 'Skin Condition'
        verbose_name_plural = 'Skin Conditions'
        ordering = ['order']
    
    def __str__(self) -> str:
        return self.name
from django.db import models

class SkinCondition(models.Model):
    '''
    Catalog of possible skin conditions.
    '''
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Skin condition name (e.g., "Normal", "Pálida", "Cianótica", "Ictérica")'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this option is available for selection'
    )
    
    class Meta:
        verbose_name = 'Skin Condition'
        verbose_name_plural = 'Skin Conditions'
        ordering = ['name']
    
    def __str__(self):
        return self.name